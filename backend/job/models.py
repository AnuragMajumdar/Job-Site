from datetime import *
from django.db import models
from django.contrib.auth.models import User

import geocoder
import os

from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator, MaxValueValidator


class jobType(models.TextChoices):
    Permanent = 'Permanent'
    Temporary = 'Temporary'
    Internship = 'Internship'

class Education(models.TextChoices):
    Bachelors = 'Bachelors'
    Masters = 'Masters'
    Phd = 'Phd'

class Industry(models.TextChoices):
    Buisness = 'Buisness'
    IT = 'Information Technology'
    Banking = 'Banking'
    Education = 'Education/Training'
    Telecommunication = 'Telecommunication'
    Others = 'Others'

class Experience(models.TextChoices):
    NO_EXPERIENCE = 'Freshers'
    ONE_YEAR = '1 Year'
    TWO_YEAR = '2_Years'
    THREE_YEAR_PLUS = '3 Years above'

def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)

class Job(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=100, null=True)
    jobType = models.CharField(
        max_length=20,
        choices = jobType.choices,
        default = jobType.Permanent
    )
    Education = models.CharField(
        max_length=30,
        choices = Education.choices,
        default = None
    )
    Industry = models.CharField(
        max_length=30,
        choices = Industry.choices,
        default = Industry.IT
    )
    Experience = models.CharField(
        max_length=20,
        choices = Experience.choices,
        default = Experience.NO_EXPERIENCE
    )
    salary = models.IntegerField(default = 1, validators = [MinValueValidator(1), MaxValueValidator(10000000)])
    positions = models.IntegerField(default=1)
    company = models.CharField(max_length=100, null=True)
    point = gismodels.PointField(default=Point(0.0, 0.0))
    last_Date = models.DateTimeField(default=return_date_time)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapquest(self.address, key = os.environ.get('GEOCODER_API'))
    
        print(g)

        lng = g.lng
        lat = g.lat

        self.point = Point(lng, lat)
        super(Job, self).save(*args, **kwargs)
