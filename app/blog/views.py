from django.http import Http404
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


class ArticleList(APIView):
    def get(self, request, format=None):
        articles = Article.objects.all()
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
    def get_object(self, article_id):
        try:
            return Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, article_id, format=None):
        article = self.get_object(article_id)
        serializer = ArticleSerializer(article)

        return Response({"article": serializer.data})   


class CommentList(APIView):
    def get(self, request, article_id, format=None):
        comments = Comment.objects.filter(article__id=article_id, level__lte=3)
        serializer = CommentSerializer(comments, many=True)

        return Response({"first_three_comments_levels": serializer.data})

    def post(self, request, article_id, format=None):
        if request.data.get('article'):
            raise APIException("don't specify article explicitly")

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise APIException('no article with this id')

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
    def get_object(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, article_id, comment_id, format=None):
        comment = self.get_object(comment_id)
        if comment.level != 2:
            serializer = CommentSerializer(comment)

            return Response({"comment": serializer.data})

        answers_tree = comment.get_descendants()
        root_serializer = CommentSerializer(comment)
        answers_tree_serializer = CommentSerializer(answers_tree, many=True)

        return Response({
                "third_level_comment": root_serializer.data,
                "next_level_comments": answers_tree_serializer.data
            })

    def post(self, request, article_id, comment_id, format=None):
        if request.data.get('article'):
            raise APIException("don't specify article explicitly")

        if request.data.get('answered_to'):
            raise APIException("don't specify comment explicitly")

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise APIException('no article with this id')

        if not self.get_object(comment_id):
            raise APIException('no comment with that id')

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