# Generated by Django 4.2 on 2023-04-26 04:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0009_newsarticle_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userarticle',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
