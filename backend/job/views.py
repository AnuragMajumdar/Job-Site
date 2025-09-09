from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max, Avg, Count

from .serializers import JobSerializers
from .models import Job
from .filters import JobsFilters

from django.shortcuts import get_object_or_404
# Create your views here.


@api_view(['GET'])
def getAllJobs(request):

    filterset = JobsFilters(request.GET, queryset = Job.objects.all().order_by('id'))

    serializer = JobSerializers(filterset.qs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getJobById(request, pk):
    job = get_object_or_404(Job, id=pk)
    serializer = JobSerializers(job, many = False)
    return Response(serializer.data)

@api_view(['POST'])
def CreateJob(request):
    data = request.data
    job = Job.objects.create(**data)
    serializer = JobSerializers(job, many = False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.jobType = request.data['jobType']
    job.Education = request.data['Education']
    job.Industry = request.data['Industry']
    job.Experience = request.data['Experience']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']

    job.save()


    serializer = JobSerializers(job, many = False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    job.delete()
    return Response({ 'message' : 'Job Deleted'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getTopicStats(request, topic):
    args = {'title__icontains' : topic}
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response({ 'message' : 'No Jobs found for this {topic}'.format(topic=topic)})
    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        min_salary = Min('salary'),
        max_salary = Max('salary'),
        avg_salary = Avg('salary'),
        avg_positions = Avg('positions'),
    )
    stats['topic'] = topic

    return Response(stats)

