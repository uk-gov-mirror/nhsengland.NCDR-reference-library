# Generated by Django 2.1.7 on 2019-02-28 14:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0009_alter_user_last_name_max_length")]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",  # noqa: E501
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.TextField(unique=True)),
                ("password", models.TextField(blank=True, null=True)),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",  # noqa: E501
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Column",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "data_type",
                    models.CharField(
                        choices=[
                            ("datetime", "datetime"),
                            ("date", "date"),
                            ("int", "int"),
                            ("bigint", "bigint"),
                            ("varchar(1)", "varchar(1)"),
                            ("varchar(2)", "varchar(2)"),
                            ("varchar(3)", "varchar(3)"),
                            ("varchar(4)", "varchar(4)"),
                            ("varchar(5)", "varchar(5)"),
                            ("varchar(6)", "varchar(6)"),
                            ("varchar(7)", "varchar(7)"),
                            ("varchar(8)", "varchar(8)"),
                            ("varchar(9)", "varchar(9)"),
                            ("varchar(10)", "varchar(10)"),
                            ("varchar(11)", "varchar(11)"),
                            ("varchar(12)", "varchar(12)"),
                            ("varchar(13)", "varchar(13)"),
                            ("varchar(14)", "varchar(14)"),
                            ("varchar(15)", "varchar(15)"),
                            ("varchar(16)", "varchar(16)"),
                            ("varchar(17)", "varchar(17)"),
                            ("varchar(18)", "varchar(18)"),
                            ("varchar(19)", "varchar(19)"),
                            ("varchar(20)", "varchar(20)"),
                            ("varchar(50)", "varchar(50)"),
                            ("varchar(100)", "varchar(100)"),
                        ],
                        max_length=255,
                    ),
                ),
                ("derivation", models.TextField(blank=True, default="")),
                (
                    "technical_check",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "is_derived_item",
                    models.NullBooleanField(
                        default=False, verbose_name="Is the item derived?"
                    ),
                ),
                ("definition_id", models.IntegerField(blank=True, null=True)),
                ("author", models.CharField(blank=True, max_length=255, null=True)),
                ("created_date_ext", models.DateField(blank=True, null=True)),
                ("link", models.URLField(blank=True, max_length=500, null=True)),
            ],
            options={"verbose_name": "Column", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Database",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.TextField()),
                ("display_name", models.TextField(blank=True, null=True)),
                ("description", models.TextField(default="")),
                ("link", models.URLField(blank=True, max_length=500, null=True)),
                ("owner", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="DataElement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(default="")),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Grouping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Schema",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.TextField()),
                (
                    "database",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schemas",
                        to="ncdr.Database",
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Table",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(default="")),
                ("link", models.URLField(blank=True, max_length=500, null=True)),
                (
                    "is_table",
                    models.BooleanField(
                        choices=[(True, "Table"), (False, "View")],
                        default=True,
                        verbose_name="Table or View",
                    ),
                ),
                (
                    "date_range",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "schema",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tables",
                        to="ncdr.Schema",
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
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
                ),
                ("is_published", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="versions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"get_latest_by": "pk"},
        ),
        migrations.AddField(
            model_name="dataelement",
            name="grouping",
            field=models.ManyToManyField(to="ncdr.Grouping"),
        ),
        migrations.AddField(
            model_name="database",
            name="version",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="databases",
                to="ncdr.Version",
            ),
        ),
        migrations.AddField(
            model_name="column",
            name="data_element",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ncdr.DataElement",
            ),
        ),
        migrations.AddField(
            model_name="column",
            name="table",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ncdr.Table"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="current_version",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="ncdr.Version",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",  # noqa: E501
                related_name="user_set",
                related_query_name="user",
                to="auth.Group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="table", unique_together={("name", "schema")}
        ),
        migrations.AlterUniqueTogether(
            name="schema", unique_together={("name", "database")}
        ),
        migrations.AlterUniqueTogether(
            name="database", unique_together={("name", "version")}
        ),
        migrations.AlterUniqueTogether(
            name="column",
            unique_together={
                ("name", "table", "data_element", "is_derived_item", "link")
            },
        ),
    ]