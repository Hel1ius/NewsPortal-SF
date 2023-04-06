from django.urls import path
from .views import NewsList, NewsDetail, SearchList, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('', NewsList.as_view(), name='NewsList'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', SearchList.as_view(), name='post_search'),
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete')
]