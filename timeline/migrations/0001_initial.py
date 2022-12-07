# Generated by Django 4.0.7 on 2022-09-30 21:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Timeline",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=500)),
                ("text", models.TextField(blank=True)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="timeline")),
            ],
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=500)),
                ("text", models.TextField(blank=True)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("timeline", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="timeline.timeline")),
            ],
        ),
        migrations.CreateModel(
            name="Fact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="timeline")),
                ("source", models.CharField(blank=True, max_length=500)),
                ("url", models.URLField(blank=True)),
                ("date", models.DateTimeField()),
                ("timeline", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="timeline.timeline")),
            ],
        ),
    ]