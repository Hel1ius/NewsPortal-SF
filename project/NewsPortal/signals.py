from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import PostCategory
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_users(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        category_names = categories.values_list('category_name', flat=True)
        subscribers = set(categories.values_list('subscribers__email', flat=True))
        post_id = instance.id
        msg = EmailMultiAlternatives(
            subject=f'NewsPortal: new post',
            body=f'Новый пост в категории {", ".join(category_names)}: http://127.0.0.1:8000/news/{post_id}/',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers,
        )
        msg.send()