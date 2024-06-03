# Generated by Django 5.0.3 on 2024-05-31 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_award_date_awarded_alter_user_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerprofile',
            name='profession',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_seller',
            field=models.BooleanField(default=True),
        ),
    ]