from django.urls import path

from . import views

app_name = "geodb"

urlpatterns = [
    # GET - Area Polygon
    path(r"areas", views.AreasView.as_view(), name="handler-area_polygon"),
    # GET - POIs
    path(r"pois", views.PointsOfInterestView.as_view(), name="handler-pois"),
    # GET - Neighbouring objects
    path(r"neighbours", views.NeighbouringFeaturesView.as_view(), name="handler-neighbours"),
]
