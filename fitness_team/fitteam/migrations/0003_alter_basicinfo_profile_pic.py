# Generated by Django 4.1.5 on 2023-02-28 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitteam', '0002_basicinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='profile_pic',
            field=models.ImageField(default='profile.jpg', upload_to=''),
        ),
    ]
