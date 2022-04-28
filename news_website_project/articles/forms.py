from django import forms

from news_website_project.articles.models import Article, Category, Photo, Comment
from news_website_project.common.mixins import BootstrapFormMixin

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)

# articles = Article.objects.all().values_list('title', 'title')
# article_list = []
# for item in articles:
#     article_list.append(item)


class CreateArticleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        article = super().save(commit=False)
        article.user = self.user
        if commit:
            article.save()
        return article

    class Meta:
        model = Article
        fields = ['title', 'description', 'category', 'main_photo']
        widgets = {
            'category': forms.Select(choices=choice_list, attrs={
                'class': 'form-control',
            }),
            'main_photo': forms.URLInput(attrs={'placeholder': 'Photo URL'}),
            'title': forms.TextInput(attrs={'placeholder': 'Add Title'})
        }


class EditArticleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Article
        fields = ['title', 'description', 'category', 'main_photo']
        widgets = {
            'category': forms.Select(choices=choice_list, attrs={
                'class': 'form-control',
            }),
            'main_photo': forms.URLInput(attrs={'placeholder': 'Photo URL'}),
            'title': forms.TextInput(attrs={'placeholder': 'Add Title'})
        }


class DeleteArticleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super()._init_bootstrap_form_controls()
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        article_photos = Photo.objects.filter(article__exact=self.instance.title)
        article_photos.delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = Article
        fields = ['title', 'description', 'category', 'main_photo']


class PhotoCreateForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        article = super().save(commit=False)
        article.user = self.user
        if commit:
            article.save()
        return article

    class Meta:
        model = Photo
        articles = Article.objects.all().values_list('title', 'title')
        article_list = []
        for item in articles:
            article_list.append(item)
        exclude = ['user']
        widgets = {
            'article': forms.Select(choices=article_list, attrs={
                'class': 'form-control',
            }),

        }


class DeletePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = []


class AddCommentForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, article_id, author, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.user = user
        self.article_id = article_id
        self.author = author

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.article_id = self.article_id
        comment.author = self.author
        if commit:
            comment.save()
        return comment

    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add your comment...'}), label='')

    class Meta:
        model = Comment
        fields = ['body']


class EditCommentForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(
                attrs={'rows': 3}
            )
        }


class DeleteCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = []
