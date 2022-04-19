from rest_framework import serializers

from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'text']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'answered_to', 'text', 'level']

    def validate_answered_to(self, comment):
        """Checks if that comment exist in article"""
        Comment.get_comment_or_404(comment.id, self.initial_data['article'])
        return comment
