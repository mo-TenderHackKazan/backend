# Generated by Django 4.2.6 on 2023-10-21 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("errors", "0002_error_eid_error_filtered_errortype_classes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="errorsummery",
            name="type",
        ),
        migrations.DeleteModel(
            name="ErrorDateAmount",
        ),
        migrations.DeleteModel(
            name="ErrorSummery",
        ),
    ]
