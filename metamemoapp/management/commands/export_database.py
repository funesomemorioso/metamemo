import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

sql = """
WITH medias AS (
  SELECT
    u.memoitem_id,
    m.media,
    m.original_url,
    m.mediatype
  FROM (
    SELECT
      i.memoitem_id,
      m.mediatype,
      MIN(i.memomedia_id) AS memomedia_id
    FROM metamemoapp_memoitem_medias AS i
      LEFT JOIN metamemoapp_memomedia AS m
        ON m.id = i.memomedia_id
    WHERE m.media IS NOT NULL
    GROUP BY i.memoitem_id, m.mediatype
  ) AS u
    LEFT JOIN metamemoapp_memomedia AS m ON
      u.memomedia_id = m.id
      AND u.mediatype = m.mediatype
),
images AS (
  SELECT memoitem_id, media, original_url
  FROM medias
  WHERE mediatype = 'IMAGE'
),
videos AS (
  SELECT memoitem_id, media, original_url
  FROM medias
  WHERE mediatype = 'VIDEO'
)
SELECT
  i.id,
  i.content_date,
  a.name AS author,
  s.name AS source,
  i.likes,
  i.interactions,
  i.shares,
  i.original_id,
  i.url,
  i.title,
  CASE
    WHEN mv.media IS NOT NULL THEN 'downloaded'
    WHEN mv.memoitem_id IS NOT NULL THEN 'not_downloaded'
    ELSE 'no_media'
  END AS video_status,
  mv.media AS video_internal_url,
  mv.original_url AS video_original_url,
  CASE
    WHEN mi.media IS NOT NULL THEN 'downloaded'
    WHEN mi.memoitem_id IS NOT NULL THEN 'not_downloaded'
    ELSE 'no_media'
  END AS image_status,
  mi.media AS image_internal_url,
  mi.original_url AS image_original_url,
  i.content
FROM metamemoapp_memoitem AS i
  LEFT JOIN videos AS mv
    ON mv.memoitem_id = i.id
  LEFT JOIN images AS mi
    ON mi.memoitem_id = i.id
  LEFT JOIN metamemoapp_metamemo AS a
    ON a.id = i.author_id
  LEFT JOIN metamemoapp_memosource AS s
    ON s.id = i.source_id
"""


class Command(BaseCommand):
    help = "Export database executing SQL directly"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        filename = Path(settings.BASE_DIR) / "dump" / f"{today}-database.csv"
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)
        print(f"Exporting to {filename}")
        with connection.cursor() as cursor, open(filename, mode="w") as fobj:
            cursor.execute(sql)
            header = [item[0] for item in cursor.description]
            writer = csv.writer(fobj)
            writer.writerow(header)
            for row in cursor.fetchall():
                writer.writerow(row)

