from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from news_website_project.accounts.models import Profile
from news_website_project.articles.forms import CreateArticleForm, EditArticleForm, DeleteArticleForm, PhotoCreateForm, \
    AddCommentForm, EditCommentForm, DeleteCommentForm, DeletePhotoForm
from news_website_project.articles.models import Article, Photo, Comment
from news_website_project.common.mixins import UserAccessMixin


# @permissions_required(required_permissions=['articles.create_adticle'])
class CreateArticleView(UserAccessMixin, CreateView):
    permission_required = 'articles.add_article'

    template_name = 'articles/Create_Article.html'
    form_class = CreateArticleForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ArticleDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'articles/Article_Details.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['full_name'] = Profile.objects.get(user_id=self.object.user_id)
        photos = Photo.objects.filter(article__exact=self.object.id)
        context['photos'] = photos
        context['comments'] = Comment.objects.filter(article_id=self.object.id)
        context['is_owner'] = self.object.user == self.request.user
        return context


class EditArticleView(UpdateView):
    # permission_required = 'articles.edit_article'

    template_name = 'articles/Edit_Article.html'
    form_class = EditArticleForm
    model = Article

    def get_success_url(self):
        return reverse_lazy('article details', kwargs={'pk': self.object.id})


def delete_article(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = DeleteArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('show home')
    else:
        form = DeleteArticleForm(instance=article)

    context = {
        'form': form
    }
    return render(request, 'articles/Delete_Article.html', context)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'articles/Add_Comment.html'
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse_lazy('article details', kwargs={'pk': self.object.article_id})

    def get_form_kwargs(self):
        author = Profile.objects.get(user_id=self.request.user)
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['article_id'] = self.kwargs['pk']
        kwargs['author'] = author
        return kwargs


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'articles/Edit_Comment.html'
    form_class = EditCommentForm

    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        return reverse_lazy('article details', kwargs={'pk': self.object.article_id})


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    template_name = 'articles/Delete_Comment.html'
    form_class = DeleteCommentForm
    model = Comment

    def get_success_url(self):
        article_id = self.object.article_id
        return reverse_lazy('article details', kwargs={'pk': article_id})

    def get_context_data(self, **kwargs):
        context = super(DeleteCommentView, self).get_context_data()
        context['comment'] = Comment.objects.get(id=self.object.id)
        return context


class AddPhotoView(UserAccessMixin, CreateView):
    permission_required = 'articles.add_photo'

    template_name = 'articles/Add_photo.html'
    model = Photo
    form_class = PhotoCreateForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeletePhotoView(DeleteView):
    template_name = 'articles/Delete_photo.html'
    form_class = DeletePhotoForm
    model = Photo
    context_object_name = 'photo'

    def get_success_url(self):
        article = list(Article.objects.filter(title__exact=self.object.article))[0]
        return reverse_lazy('article details', kwargs={'pk': article.id})

    def get_context_data(self, **kwargs):
        context = super(DeletePhotoView, self).get_context_data()
        context['photo'] = Photo.objects.get(id=self.object.id)
        return context
