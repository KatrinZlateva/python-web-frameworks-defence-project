from django.urls import path

from news_website_project.web.views import HomeView, AllNewsView, CategoriesView, CategoryArticlesView

urlpatterns = [
    path('', HomeView.as_view(), name='show home'),
    path('all-news/', AllNewsView.as_view(), name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/<int:pk>', CategoryArticlesView.as_view(), name='category'),
]
