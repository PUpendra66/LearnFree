# Generated by Django 5.0.3 on 2024-12-21 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_image_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_picture',
            new_name='avatar',
        ),
    ]
