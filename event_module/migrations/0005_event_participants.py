# Generated by Django 5.1.7 on 2025-04-04 10:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_module', '0004_remove_event_end_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, null=True, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
    ]
