from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy

from news_website_project.accounts.views import UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_website_project.web.urls')),
    path('accounts/', include('news_website_project.accounts.urls')),
    path('articles/', include('news_website_project.articles.urls')),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('show home')), name='logout user'),
]
