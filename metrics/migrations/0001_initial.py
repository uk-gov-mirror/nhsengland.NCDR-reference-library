# Generated by Django 2.1.5 on 2019-01-11 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.TextField()),
                ('definition', models.TextField()),
                ('rationale', models.TextField()),
                ('specification', models.TextField()),
                ('publication_status', models.TextField()),
                ('calculation', models.TextField()),
                ('comments', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Operand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('denominator', 'denominator'), ('numerator', 'numerator')])),
                ('value', models.TextField()),
                ('source', models.TextField()),
                ('source_address', models.TextField()),
                ('lowest_level_granularity', models.TextField()),
                ('frequency', models.TextField()),
                ('timeliness', models.TextField()),
                ('refresh_mechanism', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='operand',
            unique_together={('type', 'value', 'source', 'source_address', 'lowest_level_granularity', 'frequency', 'timeliness', 'refresh_mechanism')},
        ),
        migrations.AddField(
            model_name='metric',
            name='denominator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='denominator_metrics', to='metrics.Operand'),
        ),
        migrations.AddField(
            model_name='metric',
            name='metric_lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metrics.Lead'),
        ),
        migrations.AddField(
            model_name='metric',
            name='numerator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numerator_metrics', to='metrics.Operand'),
        ),
        migrations.AddField(
            model_name='metric',
            name='organisation_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metrics.Organisation'),
        ),
        migrations.AddField(
            model_name='metric',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metrics.Report'),
        ),
        migrations.AddField(
            model_name='metric',
            name='team_lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metrics.Team'),
        ),
        migrations.AddField(
            model_name='metric',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metrics.Theme'),
        ),
    ]
