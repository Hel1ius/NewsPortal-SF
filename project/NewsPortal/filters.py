import django_filters
from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms

class NewsFilter(FilterSet):
    date_time__gt = DateFilter(field_name='time_in',
                               widget=forms.DateInput(attrs={'type': 'date'}),
                               lookup_expr='gt',
                               label='Опубликовано после')
    class Meta:
        model = Post
        fields = {
            'header_field': ['icontains'],
            'author': ['exact']
        }