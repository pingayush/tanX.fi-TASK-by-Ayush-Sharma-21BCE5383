# Generated by Django 5.0.7 on 2024-07-27 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_alerts', '0003_alert_status_alter_alert_crypto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='status',
            field=models.CharField(default='created', max_length=20),
        ),
    ]