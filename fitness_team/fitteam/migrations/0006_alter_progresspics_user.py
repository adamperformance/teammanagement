# Generated by Django 4.1.5 on 2023-03-01 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitteam', '0005_alter_basicinfo_profile_pic_progresspics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progresspics',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
