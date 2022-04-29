from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.core.mail import send_mail
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


def contact(request):
    if request.method == 'POST':
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        message = request.POST['message']
        send_mail(
            'message from' + message_name,
            message,
            message_email,
            ['katrin.zlateva@gmail.com'],
        )
        context = {
            'message_name': message_name,

        }
        return render(request, 'web/Contact_us.html', context)
    else:
        return render(request, 'web/Contact_us.html')


def error_404(request):
    return redirect(reverse_lazy('404 page'))


