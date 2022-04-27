from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news_website_project.accounts.models import Profile
from news_website_project.articles.models import Article


UserModel = get_user_model()


class ProfileDetailsViewTests(TestCase):
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

    def test_expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed('accounts/Profile_Details.html')

    # def test_when_opening_not_existing_profile__expect_404(self):
    #     response = self.client.get(reverse('profile details', kwargs={
    #         'pk': 1,
    #     }))
    #
    #     self.assertEqual(404, response.status_code)

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)
        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'email': 'test2@test.com',
            'password': '12345qwe',
        }
        self.__create_user(**credentials)
        self.client.login(**credentials)
        response = self.__get_response_for_profile(profile)
        self.assertFalse(response.context['is_owner'])

    def test_when_user_is_owner__show_users_articles_only(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        article = self.__create_article(user)
        response = self.__get_response_for_profile(profile)
        self.assertEqual([article], list(response.context_data['articles']))

