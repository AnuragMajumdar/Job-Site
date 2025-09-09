from django_filters import rest_framework as filters
from .models import Job

class JobsFilters(filters.FilterSet):
    class Meta:
        model = Job
        fields = ('Education', 'jobType', 'Experience')