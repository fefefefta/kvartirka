from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.http import Http404


class Article(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(blank=True)

    @classmethod
    def get_articles(cls):
        return cls.objects.all()

    @classmethod
    def get_article_or_404(cls, article_id):
        try:
            return cls.objects.get(pk=article_id)
        except cls.DoesNotExist:
            raise Http404

    def get_first_comment_levels(self):
        """Returns comments below the specified level (3)"""
        return Comment.objects.filter(
                article=self,
                level__lte=Comment.EDGE_COMMENT_LEVEL
            )


class Comment(MPTTModel):
    # Because mptt counts levels from 0
    EDGE_COMMENT_LEVEL = 2

    # Field for more efficient operations on comment trees
    answered_to = TreeForeignKey(
            'self',
            on_delete=models.DO_NOTHING,
            null=True,
            blank=True,
        )
    article = models.ForeignKey(
            'Article',
            on_delete=models.CASCADE,
            blank=False,
        )
    text = models.TextField(blank=True)

    class MPTTMeta:
        parent_attr = 'answered_to'

    @classmethod
    def get_comment_or_404(cls, comment_id, article_id):
        try:
            return cls.objects.get(pk=comment_id, article__id=article_id)
        except cls.DoesNotExist:
            raise Http404

    @classmethod
    def get_comments_by_article_id(cls, article_id):
        article = Article.get_article_or_404(article_id)
        return cls.objects.filter(
                article=article,
            )
