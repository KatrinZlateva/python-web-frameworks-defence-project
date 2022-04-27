from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from news_website_project.accounts.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from news_website_project.accounts.models import Profile, NewsUser
from news_website_project.articles.models import Article


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/Create_Profile.html'
    success_url = reverse_lazy('show home')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLoginView(LoginView):
    template_name = 'accounts/Login.html'
    success_url = reverse_lazy('show home')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/Profile_Details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        articles = Article.objects.filter(user_id=self.object.user)
        context['articles'] = articles
        context['is_owner'] = self.object.user == self.request.user
        return context


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'accounts/Edit_Profile.html'
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})


class ProfileDeleteView(DeleteView):
    model = NewsUser
    template_name = 'accounts/Delete_Profile.html'
    form_class = DeleteProfileForm
    success_url = reverse_lazy('show home')
