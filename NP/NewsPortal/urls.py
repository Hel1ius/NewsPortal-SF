from django.urls import path, include
from .views import NewsListView, NewsDetailView, SearchView, PostUpdateView, PostCreateView, PostDeleteView, \
    subscribe_to_category

urlpatterns = [
    path('', NewsListView.as_view(), name='NewsList'),
    path('<int:pk>', NewsDetailView.as_view(), name='NewsId'),
    path('search/', SearchView.as_view(), name='Search'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='Update'),
    path('create/', PostCreateView.as_view(), name='Create'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='Delete'),
    path('subscribe/<int:post_id>', subscribe_to_category, name='subscribe'),
]