
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addPost", views.addPost,name="addPost"),
    path("allPosts",views.allPosts,name="allPosts"),
    path("profile",views.profile,name="profile"),
    path("follow/<str:userName>/",views.follow,name="follow"),
    path("seeProfile/<int:id>/", views.seeProfile , name="seeProfile"),
    path("unfollow/<int:user_id>/",views.unfollow , name="unfollow"),
    path("following",views.following,name="following"),
    path("edit",views.edit,name="edit"),
    path("like",views.like,name="like")
]
