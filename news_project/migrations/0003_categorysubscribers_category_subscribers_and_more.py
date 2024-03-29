# Generated by Django 4.0.5 on 2022-07-29 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_project', '0002_remove_author_author_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySubscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(through='news_project.CategorySubscribers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categorysubscribers',
            name='linked_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news_project.category'),
        ),
        migrations.AddField(
            model_name='categorysubscribers',
            name='linked_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
