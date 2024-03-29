# Generated by Django 4.0.7 on 2022-11-25 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("metamemoapp", "0003_memonews_metamemoapp_content_8a27c9_idx_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="memocontext",
            options={"ordering": ["-start_date"]},
        ),
        migrations.AlterModelOptions(
            name="memoitem",
            options={"ordering": ["-content_date"]},
        ),
        migrations.AlterModelOptions(
            name="newscover",
            options={"ordering": ["-content_date"]},
        ),
        migrations.AlterModelOptions(
            name="newsitem",
            options={"ordering": ["-content_date"]},
        ),
        migrations.AddIndex(
            model_name="memocontext",
            index=models.Index(fields=["start_date", "end_date"], name="metamemoapp_start_d_3ae90f_idx"),
        ),
    ]
