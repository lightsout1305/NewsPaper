# Generated by Django 4.0.5 on 2022-10-01 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_project', '0007_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_name_en_us',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_name_fr',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_name_ru',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='content_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='content_fr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='content_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_fr',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
