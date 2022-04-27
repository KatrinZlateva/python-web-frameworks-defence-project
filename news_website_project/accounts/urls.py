from django.urls import path

from news_website_project.accounts.views import CreateProfileView, ProfileDetailsView, ProfileEditView, \
    ProfileDeleteView

urlpatterns = [
    path('profile/create/', CreateProfileView.as_view(), name='create profile'),
    path('profile/details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>', ProfileDeleteView.as_view(), name='delete user'),
]
