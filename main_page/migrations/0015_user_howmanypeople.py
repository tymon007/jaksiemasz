# Generated by Django 2.2.6 on 2019-10-22 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0014_user_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='howManyPeople',
            field=models.IntegerField(default=0),
        ),
    ]
