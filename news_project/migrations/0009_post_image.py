# Generated by Django 4.0.5 on 2023-11-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_project', '0008_category_category_name_en_us_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
