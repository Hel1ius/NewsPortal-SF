from django.forms import ModelForm, ChoiceField, CharField

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['choice', 'header', 'content', 'categories', 'author']
