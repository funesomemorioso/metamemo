# Generated by Django 4.0.7 on 2023-07-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metamemoapp', '0007_auto_20221129_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='metamemo',
            name='telegram_handle',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
