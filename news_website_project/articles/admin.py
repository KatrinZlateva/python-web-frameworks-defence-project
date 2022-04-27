from django.contrib import admin

from news_website_project.articles.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
