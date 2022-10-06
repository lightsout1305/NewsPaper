from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import CategorySubscribers, Category, PostCategory
from NewsPaper.settings import SERVER_EMAIL


@shared_task
def weekly_content_update():
    for cat in Category.objects.all():
        for subscribe in CategorySubscribers.objects.filter(linked_category=cat):
            postcat = PostCategory.objects.filter(category=cat)
            msg = EmailMultiAlternatives(
                subject=f'Weekly content for {subscribe.linked_category} category',
                from_email=SERVER_EMAIL,
                to=[subscribe.linked_user.email, ],
            )
            html_content = render_to_string(
                'news_project/weekly_articles.html',
                {
                    'recipient': subscribe.linked_user,
                    'category': cat,
                    'week_feed': postcat,
                }
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()
