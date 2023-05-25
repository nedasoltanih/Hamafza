from django.urls import path
from . import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    path('token/', rest_views.obtain_auth_token),
    path('profile/', views.ProfileView.as_view()),
    path('my_articles/', views.ArticlesAuthorView.as_view()),
    path('my_article/<int:pk>/', views.ArticleAuthorDetail.as_view()),
    path('badges/', views.BadgesView.as_view()),
    path('authors/', views.AuthorsView.as_view()),
    path('articles/', views.ArticlesView.as_view()),
]