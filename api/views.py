from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, api_view,parser_classes
from rest_framework.views import status
from files.models import File,Faculty,Module, ModuleGroup
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from .params import name,file_type
from django.db.models import Q
from drf_yasg import openapi

from .serializers import FileSerializer,FacultySerializer,ModuleSerializer

# Create your views here.
@swagger_auto_schema(method="GET",manual_parameters=[name])
@api_view(["GET"])
def get_faculty(request):
    fac = request.GET.get("query","")
    query = Faculty.objects.filter(Q(name__icontains=fac) | Q(short__icontains=fac))
    if len(query) == 0:
        return Response({"message":"not found"},status=status.HTTP_404_NOT_FOUND)

    serializer = FacultySerializer(query,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

#module view
@swagger_auto_schema(method="GET",manual_parameters=[name])
@api_view(["GET"])
def module(request):
    name = request.GET.get("query","")
    
    query = Module.objects.filter(Q(name__icontains=name) | Q(short__icontains=name))
    print(query)
    if len(query) == 0:
        return Response({"message":"not found"},status=status.HTTP_404_NOT_FOUND)
    serializer = ModuleSerializer(query,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(["GET"])
def get_module_byID(request,id):
    queryset = get_object_or_404(Module,id=id)
    serializer = ModuleSerializer(queryset,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)
   

@api_view(["GET"])
def get_faculty_byID(request,id):
    queryset = get_object_or_404(Faculty,id=id)
    serializer = FacultySerializer(queryset,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
def get_file_byID(request,id):
    queryset = get_object_or_404(File,id=id)
    serializer = FileSerializer(queryset,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
def get_faculties(request):
    queryset = Faculty.objects.all()
    serializer = FacultySerializer(queryset,many=True)
    return Response(serializer.data)



@swagger_auto_schema(method="GET",manual_parameters=[name,file_type])
@api_view(["GET"])
def search_files(request):
    query = request.GET.get("query")
    file_type = request.GET.get("type")

    filter_q = Q(accepted=True)
    if query is not None:
        filter_q &= Q(title__icontains=query)

    if file_type is not None:
        filter_q &= Q(file_type__icontains=file_type)


    queryset = File.objects.filter(filter_q).order_by("downloads_count")
    serializer = FileSerializer(queryset,many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['file'],
    properties={
        'file': openapi.Schema(type=openapi.TYPE_FILE,format=openapi.FORMAT_BINARY)
            }
))
@parser_classes([MultiPartParser,FormParser])
@api_view(["POST"])
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



@api_view(["GET"])
def get_modules_by_group(request):
    fac = request.GET.get("fac","")
    group = request.GET.get("group","")

    faculty = get_object_or_404(Faculty,short=fac)
    module_group = get_object_or_404(ModuleGroup,short=group)
    query = Q(faculty__short=faculty.short) & Q(group__short=module_group.short)
    modules = Module.objects.filter(query)

    serializer = ModuleSerializer(modules,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)




@api_view(["GET"])
def get_file_count(request,id):
    fac = get_object_or_404(Faculty,id=id)
    response = {
        "file_count":fac.file_count(),
        "tp_count":fac.tp_file_count(),
        "td_count":fac.td_file_count(),
        "cour_count":fac.cour_file_count(),
        "other_count":fac.other_file_count(),
    }
    return Response(response,status=status.HTTP_200_OK)


@api_view(["GET"])
def get_module_count(request,id):
    fac = get_object_or_404(Module,id=id)
    response = {
        "file_count":fac.file_count(),
        "tp_count":fac.tp_file_count(),
        "td_count":fac.td_file_count(),
        "cour_count":fac.cour_file_count(),
        "other_count":fac.other_file_count(),
    }
    return Response(response,status=status.HTTP_200_OK)

