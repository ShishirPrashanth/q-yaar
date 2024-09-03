from django.db import models


class PointOfInterest(models.Model):
    name = models.CharField(max_length=200)
