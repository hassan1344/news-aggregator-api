# Generated by Django 4.2 on 2023-04-25 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0002_rename_title_newsarticle_headline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavorite',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
    ]