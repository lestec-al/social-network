# Generated by Django 3.2.9 on 2021-11-24 17:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0007_rename_avatar_avatar_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Avatar',
            new_name='Images',
        ),
    ]