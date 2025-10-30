from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/create/", views.create_post, name="create_post"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("post/<slug:slug>/delete/", views.delete_post, name="delete_post"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("my-posts/", views.user_posts, name="user_posts"),
    path("register/", views.register, name="register"),
]
