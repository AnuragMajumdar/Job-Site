from django_filters import rest_framework as filters
from .models import Job

class JobFilters(filters.FilterSet):
    class Meta:
        model = Job
        field = ('education', 'JobType', 'experience')