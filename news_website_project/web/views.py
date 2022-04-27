from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView

from news_website_project.articles.models import Article, Category


class HomeView(TemplateView):
    template_name = 'web/Index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        articles = list(Article.objects.all())
        context['articles'] = articles[0:2]
        return context


class AllNewsView(LoginRequiredMixin, ListView):
    template_name = 'web/Dashboard.html'
    model = Article
    context_object_name = 'articles'


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
        articles = Article.objects.filter(category__exact=self.object.name)
        context['articles'] = articles
        return context
