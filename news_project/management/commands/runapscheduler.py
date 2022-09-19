import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from Project.settings import SERVER_EMAIL
from news_project.models import Category, CategorySubscribers, PostCategory


logger = logging.getLogger(__name__)


def my_job():
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
                    'site': Site.objects.get_current().domain,
                    'week_feed': postcat,
                }
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")