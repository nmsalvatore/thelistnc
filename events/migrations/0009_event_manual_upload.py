# Generated by Django 5.0.3 on 2024-07-09 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0008_alter_event_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="manual_upload",
            field=models.BooleanField(default=False),
        ),
    ]
