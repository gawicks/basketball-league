# Generated by Django 4.1.2 on 2022-11-04 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_stat_last_login_alter_stat_last_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='times_logged_in',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
