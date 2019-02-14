# Generated by Django 2.0 on 2018-01-22 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("csv_schema", "0006_delete_sitedescription")]

    operations = [
        migrations.AddField(
            model_name="database",
            name="owner",
            field=models.CharField(
                choices=[("NHS Digital", "NHS Digital"), ("Various", "Various")],
                default="NHS Digital",
                max_length=255,
            ),
            preserve_default=False,
        )
    ]
