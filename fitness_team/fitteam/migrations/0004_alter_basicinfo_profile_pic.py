# Generated by Django 4.1.5 on 2023-02-28 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitteam', '0003_alter_basicinfo_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='profile_pic',
            field=models.ImageField(default='profile.jpg', upload_to='images'),
        ),
    ]