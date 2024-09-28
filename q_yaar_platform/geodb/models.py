from django.contrib.gis.db import models
from django.db.models import JSONField

OSM_SRID = 3857


class OpenStreetMapFields(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    osm_subtype = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class OpenStreetMapWheelchairDesc(models.Model):
    wheelchair = models.CharField(max_length=255)
    wheelchair_desc = models.CharField(max_length=255)

    class Meta:
        abstract = True


class OpenStreetMapAddress(models.Model):
    housenumber = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        abstract = True


class AmenityLine(
    OpenStreetMapFields, OpenStreetMapAddress, OpenStreetMapWheelchairDesc
):
    geom = models.LineStringField(srid=OSM_SRID)

    class Meta:
        db_table = "amenity_point"
        managed = False


class AmenityPoint(
    OpenStreetMapFields, OpenStreetMapAddress, OpenStreetMapWheelchairDesc
):
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "amenity_line"
        managed = False


class AmenityPolygon(
    OpenStreetMapFields, OpenStreetMapAddress, OpenStreetMapWheelchairDesc
):
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "amenity_polygon"
        managed = False


class BuildingCombinedPoint(
    OpenStreetMapFields, OpenStreetMapAddress, OpenStreetMapWheelchairDesc
):
    levels = models.IntegerField()
    height = models.DecimalField(max_digits=4, decimal_places=2)
    operator = models.CharField(max_length=255)
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "building_combined_point"
        managed = False


class LeisurePoint(OpenStreetMapFields):
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "leisure_point"
        managed = False


class LeisurePolygon(OpenStreetMapFields):
    geom = models.MultiPolygonField(srid=OSM_SRID)

    class Meta:
        db_table = "leisure_polygon"
        managed = False


class NaturalLine(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    ele = models.IntegerField()
    name = models.CharField(max_length=255)
    geom = models.LineStringField(srid=OSM_SRID)

    class Meta:
        db_table = "natural_line"
        managed = False


class NaturalPoint(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    ele = models.IntegerField()
    name = models.CharField(max_length=255)
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "natural_point"
        managed = False


class NaturalPolygon(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    ele = models.IntegerField()
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField(srid=OSM_SRID)

    class Meta:
        db_table = "natural_polygon"
        managed = False


class PlaceLine(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    boundary = models.CharField(max_length=255)
    admin_level = models.IntegerField()
    name = models.CharField(max_length=255)
    geom = models.LineStringField(srid=OSM_SRID)

    class Meta:
        db_table = "place_line"
        managed = False


class PlacePoint(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    boundary = models.CharField(max_length=255)
    admin_level = models.IntegerField()
    name = models.CharField(max_length=255)
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "place_point"
        managed = False


class PlacePolygon(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    boundary = models.CharField(max_length=255)
    admin_level = models.IntegerField()
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField(srid=OSM_SRID)

    class Meta:
        db_table = "place_polygon"
        managed = False


class POICombinedPoint(OpenStreetMapFields, OpenStreetMapAddress):
    operator = models.CharField(max_length=255)
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "poi_combined_point"
        managed = False


class POILine(OpenStreetMapFields, OpenStreetMapAddress):
    operator = models.CharField(max_length=255)
    geom = models.LineStringField(srid=OSM_SRID)

    class Meta:
        db_table = "poi_line"
        managed = False


class POIPoint(OpenStreetMapFields, OpenStreetMapAddress):
    operator = models.CharField(max_length=255)
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "poi_point"
        managed = False


class POIPolygon(OpenStreetMapFields, OpenStreetMapAddress):
    operator = models.CharField(max_length=255)
    member_ids = models.JSONField()
    geom = models.LineStringField(srid=OSM_SRID)

    class Meta:
        db_table = "poi_polygon"
        managed = False


class RoadLine(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255)
    maxspeed = models.IntegerField()
    oneway = models.SmallIntegerField()
    layer = models.IntegerField()
    tunnel = models.TextField()
    bridge = models.TextField()
    major = models.BooleanField()
    route_foot = models.BooleanField()
    route_cycle = models.BooleanField()
    route_motor = models.BooleanField()
    access = models.TextField()
    member_ids = models.JSONField()
    geom = models.MultiLineStringField(srid=OSM_SRID)

    class Meta:
        db_table = "road_line"
        managed = False


class RoadPoint(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255)
    maxspeed = models.IntegerField()
    oneway = models.SmallIntegerField()
    layer = models.IntegerField()
    tunnel = models.TextField()
    bridge = models.TextField()
    access = models.TextField()
    geom = models.PointField(srid=OSM_SRID)

    class Meta:
        db_table = "road_point"
        managed = False


class RoadPolygon(models.Model):
    osm_id = models.BigIntegerField(primary_key=True)
    osm_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255)
    maxspeed = models.IntegerField()
    oneway = models.SmallIntegerField()
    layer = models.IntegerField()
    tunnel = models.TextField()
    bridge = models.TextField()
    major = models.BooleanField()
    route_foot = models.BooleanField()
    route_cycle = models.BooleanField()
    route_motor = models.BooleanField()
    access = models.TextField()
    member_ids = models.JSONField()
    geom = models.MultiPolygonField(srid=OSM_SRID)

    class Meta:
        db_table = "road_polygon"
        managed = False
