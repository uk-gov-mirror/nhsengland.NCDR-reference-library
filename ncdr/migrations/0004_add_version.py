# Generated by Django 2.1.7 on 2019-02-15 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ncdr", "0003_move_csv_schema_models_into_ncdr")]

    operations = [
        migrations.CreateModel(
            name="Version",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
            options={"get_latest_by": "-pk"},
        )
    ]