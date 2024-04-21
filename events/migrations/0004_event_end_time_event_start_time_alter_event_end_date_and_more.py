from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):
    def split_datetime_fields(apps, schema_editor):
        Event = apps.get_model("events", "Event")

        for obj in Event.objects.all():
            start_date_local = timezone.localtime(obj.start_date)
            obj.new_start_date = start_date_local.date()
            obj.start_time = start_date_local.time()

            if obj.end_date:
                end_date_local = timezone.localtime(obj.end_date)
                obj.end_time = end_date_local.time()
                obj.new_end_date = end_date_local.date()
            else:
                obj.new_end_date = None

            obj.save()

    dependencies = [
        ("events", "0003_alter_event_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="end_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="start_time",
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="new_end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="new_start_date",
            field=models.DateField(null=True),
        ),
        migrations.RunPython(split_datetime_fields),
        migrations.RemoveField(
            model_name="event",
            name="start_date",
        ),
        migrations.RemoveField(
            model_name="event",
            name="end_date",
        ),
        migrations.AlterField(
            model_name="event",
            name="new_start_date",
            field=models.DateField(),
        ),
        migrations.RenameField(
            model_name="event",
            old_name="new_start_date",
            new_name="start_date",
            
        ),
        migrations.RenameField(
            model_name="event",
            old_name="new_end_date",
            new_name="end_date",
        )
    ]