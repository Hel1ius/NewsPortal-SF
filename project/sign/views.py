from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import BaseRegisterForm
from NewsPortal.models import Category, PostCategory


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_profile'] = user
        context['is_not_author'] = not user.groups.filter(name='authors').exists()

        categories = Category.objects.all()

        subscribers = {}
        for category in categories:
            subscribers[category.category_name] = list(category.subscribers.all())
        context['subscribers'] = subscribers

        return context


@login_required
def subscribe_to_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')
        user = request.user
        try:
            category = Category.objects.get(category_name=category_name)
            category.subscribers.add(user)
            messages.success(request, f'Вы успешно подписались на рассылку в категории {category_name}!')
        except Category.DoesNotExist:
            messages.error(request, f'Категория {category_name} не найдена.')
        return redirect('profile')

@login_required
def unsubscribe_from_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')
        user = request.user
        try:
            category = Category.objects.get(category_name=category_name)
            category.subscribers.remove(user)
            messages.success(request, f'Вы успешно отписались от рассылки в категории {category_name}!')
        except Category.DoesNotExist:
            messages.error(request, f'Категория {category_name} не найдена.')
        return redirect('profile')


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')

# @login_required
# def subscribe(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     category.subscribers.add(request.user)
#     category.save()
#     return redirect('/', {'category': category})
#
# @login_required
# def unsubscribe(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     category.subscribers.remove(request.user)
#     return redirect('/', {'category': category})

# class ProfileInfoAuthor(LoginRequiredMixin, TemplateView):
#     template_name = 'profile/profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_author'] = not self.request.group.filter(name='authors').exists()
#         return context
