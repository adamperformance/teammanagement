# Generated by Django 4.1.5 on 2023-03-01 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitteam', '0006_alter_progresspics_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progresspics',
            name='date',
            field=models.DateField(),
        ),
    ]