from mptt.models import MPTTModel, TreeForeignKey
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(blank=True)


class Comment(MPTTModel):
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
