from django.urls import path, include

import blog.urls


urlpatterns = [
    path('', include(blog.urls))
]