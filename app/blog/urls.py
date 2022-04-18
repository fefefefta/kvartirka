from django.urls import path

from .views import (ArticleList, ArticleDetail, CommentList, 
	CommentDetail)


urlpatterns = [
	path('articles/', ArticleList.as_view()),
	path('articles/<int:article_id>/', ArticleDetail.as_view()),
	path('articles/<int:article_id>/comments/', CommentList.as_view()),
	path('articles/<int:article_id>/comments/<comment_id>/', CommentDetail.as_view()),
]
