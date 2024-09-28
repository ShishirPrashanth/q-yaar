import logging

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.custom_throttlers import TokenLessAuthAPIThrottleBurst, TokenLessAuthAPIThrottleSustained
from common.decorators import validate_profile
from common.permissions import ActivePermission
from common.response import get_standard_response

from geodb.services.core import (
        svc_geo_get_areas,
        svc_geo_get_notable_points,
        svc_geo_get_neighbours
)


class AreasView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".AreasView")
    permission_classes = (AllowAny,)

    @validate_profile(logger=logger, allowed_roles=[])
    def get(self, request, **kwargs):
        error, response = svc_geo_get_areas(search_string=request.data['search_string'], admin_level=request.data['admin_level'])
        return get_standard_response(error, response)


class PointsOfInterestView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".PointsOfInterestView")
    permission_classes = (AllowAny,)

    @validate_profile(logger=logger, allowed_roles=[])
    def get(self, request, **kwargs):
        error, response = svc_geo_get_notable_points(
            osm_types=request.data['osm_types'],
            n_points=request.data['n_points'],
            play_area=request.data['play_area']
        )
        return get_standard_response(error, response)


class NeighbouringFeaturesView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".PointsOfInterestView")
    permission_classes = (AllowAny,)

    @validate_profile(logger=logger, allowed_roles=[])
    def get(self, request, **kwargs):
        error, response = svc_geo_get_neighbours(
            pois=request.data['POIs'],
            osm_types=request.data['osm_types'],
            n_neighbours=request.data['n_neighbours'],
            play_area=request.data['play_area']
        )
        return get_standard_response(error, response)
