from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from news_website_project.accounts.models import Profile, NewsUser
from news_website_project.articles.models import Article
from news_website_project.common.helpers import BootstrapFormMixin


class CreateProfileForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LEN,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LEN
    )
    email = forms.EmailField(
    )
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
    )
    picture = forms.URLField()
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            picture=self.cleaned_data['picture'],
            description=self.cleaned_data['description'],
            user=user)

        if commit:
            profile.save()
            return user

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'gender', 'date_of_birth', 'picture', 'description']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Enter last name'}),
            'picture': forms.TextInput(
                attrs={'placeholder': 'Enter URL'}),
        }


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        exclude = ['email', 'user']
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 3}
            )
        }


class DeleteProfileForm(forms.ModelForm):

    def save(self, commit=True):
        self.instance.delete()
        Article.objects.filter(user_id=self.instance.id).delete()
        return self.instance

    class Meta:
        model = NewsUser
        fields = ()
