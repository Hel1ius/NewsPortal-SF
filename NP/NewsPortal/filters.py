from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter
from django import forms

from .models import Post, Author


class PostFilter(FilterSet):
    model = Post
    header = CharFilter(field_name='header', lookup_expr='icontains', label='Заголовок')
    author = ModelChoiceFilter(queryset=Author.objects.all(), label='Автор')
    date_time__gt = DateFilter(field_name='time_in',
                               widget=forms.DateInput(attrs={'type': 'date'}),
                               lookup_expr='gt',
                               label='Опубликовано после')