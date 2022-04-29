from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from news_website_project.accounts.models import Profile
from news_website_project.accounts.validators import validate_year, validate_only_characters
from news_website_project.articles.models import Article, Comment

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

    VALID_COMMENT_DATA = {
        'body': 'test text',
        'date_added': date.today(),
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

    def __create_comment(self, article, user):
        comment = Comment.objects.create(
            **self.VALID_COMMENT_DATA,
            article=article,
            user=user,
        )
        comment.save()
        return comment

    def test_expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed('accounts/Profile_Details.html')

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

    def test_edit_form_works_correctly(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('edit profile', kwargs={'pk': user.pk}), data={
            'pk': user.pk,
            'first_name': 'Jimmy',
            'last_name': 'Doe',
            'gender': Profile.MALE,
            'date_of_birth': '1995-03-11',
            'picture': 'http://test-pic.com'
        })
        updated_user_profile = Profile.objects.get(pk=user.pk)
        self.assertEqual('Jimmy', updated_user_profile.first_name)

    def test_profile_details__when_wrong_url_used_expect_302(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        response = self.client.get('accounts/profile/detailz/1')
        self.assertEqual(response.status_code, 302)

    def test_delete_profile__delete_all_articles_or_comments_added_by_the_user(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        article = self.__create_article(user)
        comment = self.__create_comment(article, user)
        user.delete()
        artciels = Article.objects.first()
        comments = Comment.objects.first()
        profiles = Profile.objects.first()
        self.assertIsNone(artciels)
        self.assertIsNone(comments)
        self.assertIsNone(profiles)

    def test_year_validator__throws_error_with_incorrect_year(self):
        year = date(1500, 3, 11)
        self.assertRaises(ValidationError, validate_year, year)

    def test_only_characters_validator__throws_error_with_number(self):
        name = 'Brun0'
        self.assertRaises(ValidationError, validate_only_characters, name)

    def test_only_characters_validator__throws_error_with_special_symbol(self):
        name = 'Brun#'
        self.assertRaises(ValidationError, validate_only_characters, name)

    def test_only_characters_validator__throws_error_with_space(self):
        name = 'Brun o'
        self.assertRaises(ValidationError, validate_only_characters, name)