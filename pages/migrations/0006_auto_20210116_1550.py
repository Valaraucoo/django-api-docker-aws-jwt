# Generated by Django 3.1.4 on 2021-01-16 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20210116_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='services_1_title',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='page',
            name='services_1_type',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='page',
            name='services_2_title',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='page',
            name='services_2_type',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='page',
            name='services_3_title',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='page',
            name='services_3_type',
            field=models.CharField(default='', max_length=30),
        ),
    ]
