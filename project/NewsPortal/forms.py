from django.forms import ModelForm, BooleanField
from .models import Post

class PostForm(ModelForm):
    check_box = BooleanField(label='Подтвердить')

    class Meta:
        model = Post
        fields = ['selection_field', 'header_field', 'text_field', 'author', 'categories', 'check_box']