from django.http import Http404
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


class ArticleList(APIView):
    def get(self, request, format=None):
        articles = Article.get_articles()
        serializer = ArticleSerializer(articles, many=True)

        return Response({"articles": serializer.data})

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                    {"new_article": serializer.data},
                    status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    def get(self, request, article_id, format=None):
        article = Article.get_article_or_404(article_id)
        article_serializer = ArticleSerializer(article)

        comments = article.get_first_comment_levels()
        comments_serializer = CommentSerializer(comments, many=True)

        return Response(
                {"article": article_serializer.data, 
                 "comments": comments_serializer.data}
            )


class CommentList(APIView):
    def get(self, request, article_id, format=None):
        comments = Comment.get_comments_by_article_id(article_id)
        serializer = CommentSerializer(comments, many=True)

        return Response({"comments": serializer.data})

    def post(self, request, article_id, format=None):
        # article_id is taken from the request URL
        if request.data.get('article'):
            raise APIException("don't specify article explicitly")

        request.data['article'] = article_id

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                    {"new_comment": serializer.data},
                    status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def get(self, request, article_id, comment_id, format=None):
        comment = Comment.get_comment_or_404(comment_id, article_id)

        if comment.level != Comment.EDGE_COMMENT_LEVEL:
            serializer = CommentSerializer(comment)

            return Response({"comment": serializer.data})

        # Response with comment tree with root in third level comment  
        answers_tree = comment.get_descendants()
        root_serializer = CommentSerializer(comment)
        answers_tree_serializer = CommentSerializer(answers_tree, many=True)

        return Response({
                "third_level_comment": root_serializer.data,
                "next_level_comments": answers_tree_serializer.data
            })

    def post(self, request, article_id, comment_id, format=None):
        # Theese params are taken from the request URL
        if request.data.get('article') or request.data.get('answered_to'):
            raise APIException("don't specify article and parent explicitly")

        # To check existance of that comment from that article
        Comment.get_comment_or_404(comment_id, article_id)

        request.data['article'] = article_id
        request.data['answered_to'] = comment_id

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                    {"comment": serializer.data},
                    status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
