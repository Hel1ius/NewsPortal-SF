from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, ProfileView, upgrade_me, subscribe_to_category, unsubscribe_from_category

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('subscribe/', subscribe_to_category, name='subscribe'),
    path('unsubscribe/', unsubscribe_from_category, name='unsubscribe')
]