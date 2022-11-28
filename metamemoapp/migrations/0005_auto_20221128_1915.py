import json

from django.db import migrations, transaction
from tqdm import tqdm


def transform_raw_to_json(apps, schema_editor):
    MemoItem = apps.get_model("metamemoapp", "MemoItem")
    objs = MemoItem.objects.filter(raw__isnull=False)
    changed = 0
    with transaction.atomic():
        for obj in tqdm(objs, total=objs.count()):
            raw = obj.raw
            if isinstance(raw, str):
                changed += 1
                obj.raw = json.loads(raw)
                obj.save()
    print(f"{changed} objects changed")


class Migration(migrations.Migration):

    dependencies = [
        ('metamemoapp', '0004_alter_memocontext_options_alter_memoitem_options_and_more'),
    ]

    operations = [
        migrations.RunPython(transform_raw_to_json)
    ]
