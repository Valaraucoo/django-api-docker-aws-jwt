# Generated by Django 3.1.4 on 2021-02-07 15:47

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='defaults/user-profile.png', upload_to=users.models.get_file_path),
        ),
    ]
