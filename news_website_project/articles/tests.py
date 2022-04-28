from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from news_website_project.accounts.models import Profile
from news_website_project.articles.models import Article, Comment

UserModel = get_user_model()


class ArticleViewsTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@test.com',
        'password': '123qweasd'
    }

    VALID_PROFILE_DATA = {
        'first_name': 'John',
        'last_name': 'Doe',
        'gender': Profile.MALE,
        'date_of_birth': '1995-03-11',
        'picture': 'http://test-pic.com'
    }

    VALID_ARTICLE_DATA = {
        'title': 'Test title',
        'description': 'test description',
        'published_date': date.today(),
        'category': 'Lifestyle',
        'main_photo': 'http://another-test-photo.com'
    }

    @staticmethod
    def __create_user(**credentials):
        return UserModel.objects.create_user(**credentials)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return user, profile

    def __create_article(self, user):
        article = Article.objects.create(
            **self.VALID_ARTICLE_DATA,
            user=user,
        )
        article.save()
        return article

    def test_correct_profile_id_added_to_the_article(self):
        user, _ = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        article = self.__create_article(user)
        response = self.client.get(reverse('article details', kwargs={'pk': article.pk}))
        self.assertEqual(user, response.context['user'])

    def test_shows_correct__author_full_name_in_details_view(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        article = self.__create_article(user)
        response = self.client.get(reverse('article details', kwargs={'pk': article.pk}))
        self.assertEqual(user.profile, response.context['full_name'])

    def test_creates_comment__shows_correct_relation_to_article(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        article = self.__create_article(user)
        comment = Comment.objects.create(**{
            'body': 'test text',
            'date_added': date.today(),
            'article': article,
            'user': user
        })
        current_comment = Comment.objects.first()
        self.assertEqual(comment.article, current_comment.article)

    def test_shows_correct_comments_for_specific_article(self):
        user, _ = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        article = self.__create_article(user)
        comment = Comment.objects.create(**{
            'body': 'test text',
            'date_added': date.today(),
            'article': article,
            'user': user
        })
        response = self.client.get(reverse('article details', kwargs={'pk': article.pk}))
        self.assertEqual([comment], list(response.context_data['comments']))

    def test_add_photo_to_specific_article(self):
        pass