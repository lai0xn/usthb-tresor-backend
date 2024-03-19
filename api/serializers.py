from django.shortcuts import get_object_or_404
from rest_framework import serializers
from files.models import File,Module,Faculty
from rest_framework.exceptions import ValidationError



class ModuleSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Module
        fields=('id','name','short','file_set','cour_file_count','group','drive_id','file_count','tp_file_count','td_file_count','exam_file_count','other_file_count','cour_drive_id','tp_drive_id','td_drive_id','other_drive_id',"exam_drive_id")
        depth=1

   


class FacultySerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()
    class Meta:
        model = Faculty
        fields = ('id','name','short','modules','file_count','cour_file_count','tp_file_count','td_file_count','exam_file_count','other_file_count')
        depth=2
    def get_modules(self,obj):
        serializer = ModuleSerializer(obj.modules,many=True)
        return serializer.data

class FileSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    module_id = serializers.IntegerField()
    class Meta:
        model = File
        fields='__all__'

    def get_file_name(self, obj):
        return obj.file_name
    def get_module(self,obj):
        data = {"id":obj.module.id,"name":obj.module.name} 
        return data


    def create(self,validated_data,**kwargs):
        module_id = validated_data.get("module_id")  
        module = get_object_or_404(Module,id=module_id)
        file = File.objects.create(**validated_data,module=module)
        return file


