# Generated by Django 2.2.16 on 2020-10-11 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0020_auto_20201011_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]