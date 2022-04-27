from django.urls import path

from news_website_project.articles.views import CreateArticleView, ArticleDetailsView, EditArticleView, \
    delete_article, AddPhotoView, AddCommentView, EditCommentView, DeleteCommentView, DeletePhotoView

urlpatterns = [
    path('create/', CreateArticleView.as_view(), name='create article'),
    path('details/<int:pk>', ArticleDetailsView.as_view(), name='article details'),
    path('edit/<int:pk>', EditArticleView.as_view(), name='edit article'),
    path('delete/<int:pk>', delete_article, name='delete article'),
    path('add-photo/', AddPhotoView.as_view(), name='add photo'),
    path('delete-photo/<int:pk>', DeletePhotoView.as_view(), name='delete photo'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add comment'),
    path('<int:pk>/edit-comment/', EditCommentView.as_view(), name='edit comment'),
    path('<int:pk>/delete-comment/', DeleteCommentView.as_view(), name='delete comment'),
]
