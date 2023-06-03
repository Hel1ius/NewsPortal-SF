import time

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from .models import Post, Category


# Отправка только созданного поста
@shared_task
def send_new_post(post_id, header, text, subscribers):
    msg = EmailMultiAlternatives(
        subject=f'NewsPortal: Новый пост {header}',
        body=f"Краткое содержание поста: '{text[:50]}'. Ссылка на пост 127.0.0.1:8000/news/{post_id}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.send()


# Отправка постов за последнюю неделю
@shared_task
def send_posts_week():
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    posts = Post.objects.filter(time_in__range=(start_of_week, end_of_week))
    emails = User.objects.values_list('email', flat=True)
    html_content = render_to_string('posts/posts_last_week.html', {'link': settings.SITE_URL, 'posts': posts})
    msg = EmailMultiAlternatives(
        subject='Посты за последнюю неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emails,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()