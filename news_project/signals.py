from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from .models import PostCategory, CategorySubscribers
from NewsPaper.settings import SERVER_EMAIL


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.postcategory_set.all():
            for subscribe in CategorySubscribers.objects.filter(linked_category_id=cat.category_id):
                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.content,
                    from_email=SERVER_EMAIL,
                    to=[subscribe.linked_user.email, ],
                )
                html_content = render_to_string(
                    'news_project/notification.html',
                    {
                        'title': instance.title,
                        'recipient': subscribe.linked_user,
                        'content': instance.content,
                        'pk': instance.id,
                        'site': Site.objects.get_current().domain
                    }
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()

                print(f'Тема письма: {instance.title}\nСодержание: {instance.content}')
                print(f'Уведомление отослано подписчику {subscribe.linked_user} на почту {subscribe.linked_user.email} на тему {subscribe.linked_category}')

