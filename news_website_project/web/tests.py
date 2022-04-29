from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news_website_project.accounts.models import Profile
from news_website_project.articles.models import Article

UserModel = get_user_model()


class GeneralViewsTests(TestCase):
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

    def test_home_shows_only_2_articles(self):
        user, profile = self.__create_valid_user_and_profile()
        article1 = self.__create_article(user)
        article2 = Article.objects.create(
            title='Test title 2',
            description='test description',
            published_date=date.today(),
            category='Lifestyle',
            main_photo='http://another-test-photo.com',
            user=user,
        )
        article3 = Article.objects.create(
            title='Test title 3',
            description='test description',
            published_date=date.today(),
            category='Lifestyle',
            main_photo='http://another-test-photo.com',
            user=user,
        )
        response = self.client.get(reverse('show home'))
        self.assertEqual(2, len(response.context['articles']))


