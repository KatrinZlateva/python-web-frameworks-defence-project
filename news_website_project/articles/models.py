from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from news_website_project.accounts.models import Profile
from news_website_project.articles.validators import MaxSizeInMbValidator

UserModel = get_user_model()


class Article(models.Model):
    TITLE_MAX_LEN = 50
    TITLE_MIN_LEN = 2

    FILE_MAX_SIZE = 10
    CATEGORY_MAX_LEN = 50

    FILE_MAX_SIZE_IN_MB = 10
    UPLOAD_TO_DIR = 'article_photos/'

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        unique=True,
        validators=(
            MinLengthValidator(TITLE_MIN_LEN),
        ),
    )

    description = models.TextField(
        null=False,
        blank=False,
    )

    published_date = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    likes = models.ManyToManyField(
        UserModel,
        related_name='article_post'
    )

    category = models.CharField(
        max_length=CATEGORY_MAX_LEN,
    )

    main_photo = models.URLField(
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title}  |  {self.user}'


class Photo(models.Model):
    ARTICLE_MAX_LEN = 50
    FILE_MAX_SIZE_IN_MB = 10
    UPLOAD_TO_DIR = 'article_photos/'

    photo = models.URLField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    article = models.CharField(
        max_length=ARTICLE_MAX_LEN,
        null=False,
        blank=False,
    )


class Category(models.Model):
    NAME_MAX_LEN = 50
    name = models.CharField(
        max_length=NAME_MAX_LEN,
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    AUTHOR_MAX_LEN = 50
    body = models.TextField()

    author = models.CharField(
        max_length=AUTHOR_MAX_LEN,
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )

    likes = models.ManyToManyField(
        UserModel,
        default=0,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='user_comment',
    )