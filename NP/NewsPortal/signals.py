from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import  send_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_news_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.categories.all().values_list('name', flat=True)
        subscribers = list(set(categories.values_list('subscribers__email', flat=True)))
        post_id = instance.id
        header = instance.header
        text = instance.content
        send_new_post.delay(post_id, header, text, subscribers)

