from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import status
from files.models import File,Faculty,Module
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from .serializers import FileSerializer,FacultySerialzer,ModuleSerializer

# Create your views here.

@api_view(["GET"])
def get_faculty(request):
    fac = request.GET.get("name","")
    query = get_object_or_404(Faculty,name=fac)
    serializer = FacultySerialzer(query,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["GET"])
def module(request):
    name = request.GET.get("name","")
    query = get_object_or_404(Module,name=name)
    serializer = ModuleSerializer(query,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
def get_faculties(request):
    queryset = Faculty.objects.all()
    serializer = FacultySerialzer(queryset,many=True)
    return Response(serializer.data)


@api_view(["GET"])
def search_files(request):
    query = request.GET.get("q")
    file_type = request.GET.get("type")

    filter_q = Q(accepted=True)
    if query is not None:
        filter_q &= Q(title__icontains=query)

    if file_type is not None:
        filter_q &= Q(file_type__icontains=file_type)


    queryset = File.objects.filter(filter_q).order_by("downloads_count")
    serializer = FileSerializer(queryset,many=True)
    return Response(serializer.data)


@api_view(["PUT"])
def upload_file(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"file uploaded successfully"},status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def download_file(request,id):
    file_instance = get_object_or_404(File,id=id)
    file_path = file_instance.file.path

    with open(file_path,'rb') as file:
        response = HttpResponse(file.read(),content_type='application/octet-stream')

        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_instance.file_name)
    return response

