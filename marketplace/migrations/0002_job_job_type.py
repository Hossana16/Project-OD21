# Generated by Django 5.0.3 on 2024-06-03 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('freelance', 'freelance'), ('full_time', 'full time'), ('part time', 'part_time'), ('internship', 'internship')], default='full_time', max_length=15),
        ),
    ]
