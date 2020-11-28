# blog/urls.py

from django.urls import path

from blog.views import (
    IndexView,
    CategoryListView,
    CategoryPostView,
    comment_approve,
    comment_remove,
    CommentFormView,
    PostDetailView,
    reply_approve,
    reply_remove,
    ReplyFormView,
    SearchPostView,
    TagListView,
    TagPostView,
)

from .views import ContactFormView, ContactResultView

from . import views

from django.contrib.flatpages import views


app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<str:category_slug>/',
         CategoryPostView.as_view(), name='category_post'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
    path('comment/<int:pk>/', CommentFormView.as_view(), name='comment_form'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('reply/<int:pk>/approve/', reply_approve, name='reply_approve'),
    path('reply/<int:pk>/remove/', reply_remove, name='reply_remove'),
    path('reply/<int:pk>/', ReplyFormView.as_view(), name='reply_form'),
    path('search/', SearchPostView.as_view(), name='search_post'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tag/<str:tag_slug>/', TagPostView.as_view(), name='tag_post'),
    path('contact/', ContactFormView.as_view(), name='contact_form'),
    path('contact_result/', ContactResultView.as_view(), name='contact_result'),
]


urlpatterns += [
    path('about/', views.flatpage),
]
