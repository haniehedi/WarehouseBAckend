# Generated by Django 5.1.2 on 2024-10-23 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_full_name_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
