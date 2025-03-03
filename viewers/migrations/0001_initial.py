# Generated by Django 4.1.4 on 2025-02-12 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_id', models.IntegerField()),
                ('period_start', models.DateTimeField()),
                ('period_start_date', models.DateField()),
                ('period_start_time', models.TimeField()),
                ('very_happy', models.FloatField()),
                ('happy', models.FloatField()),
                ('neutral', models.FloatField()),
                ('unhappy', models.FloatField()),
                ('very_unhappy', models.FloatField()),
                ('gender', models.IntegerField()),
                ('age', models.IntegerField()),
                ('dwell_time_in_tenths_of_sec', models.IntegerField()),
                ('attention_time_in_tenths_of_sec', models.IntegerField()),
                ('age_value', models.IntegerField()),
            ],
        ),
    ]
