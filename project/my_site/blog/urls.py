from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path(
        "posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"
    ),
    path("read-later", views.ReadLaterView.as_view(),name="read-later"),
    path("add-posts",views.AddPostView.as_view(),name="add-posts"),
    path("registration/login/",views.LoginView.as_view(), name="login"),
    path("registration/register/",views.RegisterView.as_view(), name="register"),
    path('registration/logout/', views.LogoutView.as_view(), name='logout'),
]
