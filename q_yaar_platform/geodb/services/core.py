import logging

from django.contrib.gis.measure import D
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry
from itertools import chain

from geodb.models import PlacePolygon, POICombinedPoint, RoadLine, RoadPoint

from .error_codes import ErrorCode

# skipping buildings for now
VALID_OSM_POI_TYPES = [
    "shop",
    "amenity",
    "leisure",
    "natural",
    "man_made",
    "tourism",
    "historic",
]


def svc_geo_get_areas(search_string: str, admin_level: int):
    """
    Get areas which match the name given
    """

    place_polygons = PlacePolygon.objects.filter(
        name=search_string, admin_level=admin_level
    )

    if not place_polygons:
        return ErrorCode(ErrorCode.OBJECT_NOT_FOUND), None
    return ErrorCode(ErrorCode.SUCCESS), serialize(
        "geojson",
        place_polygons,
        geometry_field="geom",
        fields=["name", "admin_level", "osm_type", "boundary"],
    )


def svc_geo_get_notable_points(osm_types: list[str], n_points: int, play_area):
    """
    Get all notable points with associated tags

    Parameters
    ----------
    osm_types: list[str]
        OSM objects to be considered. E.g. `items = ['leisure', 'buildings', 'historic', 'tourism']`
        will match on parks, buildings, memorials and tourist attractions.
    n_points: int
        The number of points to return
    play_area: polygon
        The area inside which

    Returns
    -------
    list
        A list of at most `n_points` from each category in `items`
    """

    assert n_points > 0, "Expected at least 1 item to be queried"

    for osm_type in osm_types:
        assert osm_type in VALID_OSM_POI_TYPES, "Recieved invalid osm_type"

    play_area_geom = GEOSGeometry(str(play_area["features"][0]["geometry"]))

    pois = POICombinedPoint.objects.filter(
        osm_type__in=osm_types, geom__intersects=play_area_geom
    ).order_by("?")[:n_points]
    print(len(pois))
    if not pois:
        return ErrorCode(ErrorCode.OBJECT_NOT_FOUND), None

    serialized_pois = serialize("geojson", pois, geometry_field="geom")
    return ErrorCode(ErrorCode.SUCCESS), serialized_pois


def svc_geo_get_neighbours(
    pois, osm_types: list[str], n_neighbours: int, play_area, dist=D(m=100)
):
    """
    Get all notable points with associated tags

    Parameters
    ----------
    pois: list[geojson]
        OSM objects to find neighbours for
    osm_types: list[str]
        OSM objects to be considered. E.g. `items = ['leisure', 'buildings', 'historic', 'tourism']`
        will match on parks, buildings, memorials and tourist attractions.
    n_neighbours: int
        The number of points to return
    play_area: polygon
        The area inside which
    dist: Distance
        Max distance to consider as neighbour

    Returns
    -------
    list
        A list of at most `n_points` from each category in `items`
    """
    assert n_neighbours > 0

    play_area_geom = GEOSGeometry(str(play_area["features"][0]["geometry"]))
    poi_geom = GEOSGeometry(str(pois["geometry"]))
    nearby_roads = RoadLine.objects.filter(
        geom__distance_lt=(poi_geom, dist),
        name__isnull=False,
        geom__intersects=play_area_geom,
    ).order_by("?")[:n_neighbours]
    nearby_junctions = RoadPoint.objects.filter(
        geom__distance_lt=(poi_geom, dist),
        name__isnull=False,
        geom__intersects=play_area_geom,
    ).order_by("?")[:n_neighbours]

    neighbours = list(chain(nearby_roads, nearby_junctions))

    if not neighbours:
        return ErrorCode(ErrorCode.OBJECT_NOT_FOUND), None

    serialized_neighbours = serialize("geojson", neighbours, geometry_field="geom")
    return ErrorCode(ErrorCode.SUCCESS), serialized_neighbours
