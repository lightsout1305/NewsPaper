# Generated by Django 4.0.5 on 2022-08-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_project', '0006_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
