# Generated by Django 3.1.4 on 2021-01-10 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0005_auto_20210110_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to=settings.AUTH_USER_MODEL),
        ),
    ]
