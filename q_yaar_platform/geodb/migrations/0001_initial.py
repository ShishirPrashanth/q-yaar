# Generated by Django 5.0.7 on 2024-09-28 16:01

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AmenityLine",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("wheelchair", models.CharField(max_length=255)),
                ("wheelchair_desc", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.LineStringField(srid=3857),
                ),
            ],
            options={
                "db_table": "amenity_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AmenityPoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("wheelchair", models.CharField(max_length=255)),
                ("wheelchair_desc", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "amenity_line",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AmenityPolygon",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("wheelchair", models.CharField(max_length=255)),
                ("wheelchair_desc", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "amenity_polygon",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="BuildingCombinedPoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("wheelchair", models.CharField(max_length=255)),
                ("wheelchair_desc", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("levels", models.IntegerField()),
                ("height", models.DecimalField(decimal_places=2, max_digits=4)),
                ("operator", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "building_combined_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="LeisurePoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "leisure_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="LeisurePolygon",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857),
                ),
            ],
            options={
                "db_table": "leisure_polygon",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="NaturalLine",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("ele", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.LineStringField(srid=3857),
                ),
            ],
            options={
                "db_table": "natural_line",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="NaturalPoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("ele", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "natural_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="NaturalPolygon",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("ele", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857),
                ),
            ],
            options={
                "db_table": "natural_polygon",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PlaceLine",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("boundary", models.CharField(max_length=255)),
                ("admin_level", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.LineStringField(srid=3857),
                ),
            ],
            options={
                "db_table": "place_line",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PlacePoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("boundary", models.CharField(max_length=255)),
                ("admin_level", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "place_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PlacePolygon",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("boundary", models.CharField(max_length=255)),
                ("admin_level", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857),
                ),
            ],
            options={
                "db_table": "place_polygon",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="POICombinedPoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("operator", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "poi_combined_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="POILine",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("operator", models.CharField(max_length=255)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.LineStringField(srid=3857),
                ),
            ],
            options={
                "db_table": "poi_line",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="POIPoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("operator", models.CharField(max_length=255)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "poi_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="POIPolygon",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("osm_subtype", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("housenumber", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postcode", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("operator", models.CharField(max_length=255)),
                ("member_ids", models.JSONField()),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.LineStringField(srid=3857),
                ),
            ],
            options={
                "db_table": "poi_polygon",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="RoadLine",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("ref", models.CharField(max_length=255)),
                ("maxspeed", models.IntegerField()),
                ("oneway", models.SmallIntegerField()),
                ("layer", models.IntegerField()),
                ("tunnel", models.TextField()),
                ("bridge", models.TextField()),
                ("major", models.BooleanField()),
                ("route_foot", models.BooleanField()),
                ("route_cycle", models.BooleanField()),
                ("route_motor", models.BooleanField()),
                ("access", models.TextField()),
                ("member_ids", models.JSONField()),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiLineStringField(srid=3857),
                ),
            ],
            options={
                "db_table": "road_line",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="RoadPoint",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("ref", models.CharField(max_length=255)),
                ("maxspeed", models.IntegerField()),
                ("oneway", models.SmallIntegerField()),
                ("layer", models.IntegerField()),
                ("tunnel", models.TextField()),
                ("bridge", models.TextField()),
                ("access", models.TextField()),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=3857)),
            ],
            options={
                "db_table": "road_point",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="RoadPolygon",
            fields=[
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("osm_type", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("ref", models.CharField(max_length=255)),
                ("maxspeed", models.IntegerField()),
                ("oneway", models.SmallIntegerField()),
                ("layer", models.IntegerField()),
                ("tunnel", models.TextField()),
                ("bridge", models.TextField()),
                ("major", models.BooleanField()),
                ("route_foot", models.BooleanField()),
                ("route_cycle", models.BooleanField()),
                ("route_motor", models.BooleanField()),
                ("access", models.TextField()),
                ("member_ids", models.JSONField()),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857),
                ),
            ],
            options={
                "db_table": "road_polygon",
                "managed": False,
            },
        ),
    ]
