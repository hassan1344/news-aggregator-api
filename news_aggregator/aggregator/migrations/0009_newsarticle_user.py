# Generated by Django 4.2 on 2023-04-25 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0008_userarticle_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='user',
            field=models.CharField(default='', max_length=50),
        ),
    ]
