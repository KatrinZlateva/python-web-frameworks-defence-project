from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from news_website_project.articles.models import Article, Category


class HomeView(TemplateView):
    template_name = 'web/Index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        articles = list(Article.objects.all().order_by('-published_date'))
        context['articles'] = articles[0:4]
        return context


class AllNewsView(ListView):
    template_name = 'web/Dashboard.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(AllNewsView, self).get_context_data()
        articles = Article.objects.all().order_by('-published_date')
        context['articles'] = articles
        return context


class CategoriesView(ListView):
    template_name = 'web/Categories.html'
    model = Category
    context_object_name = 'categories'


class CategoryArticlesView(DetailView):
    template_name = 'articles/Category_Articles.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryArticlesView, self).get_context_data()
        articles = Article.objects.filter(category__exact=self.object.name).order_by('-published_date')
        context['articles'] = articles
        return context


def error_404(request):
    return redirect(reverse_lazy('404 page'))
