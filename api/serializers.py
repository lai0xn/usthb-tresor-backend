from django.shortcuts import get_object_or_404
from rest_framework import serializers
from files.models import File,Module,Faculty
from rest_framework.exceptions import ValidationError


class ModuleSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Module
        fields=('id','name','file_set')
        depth=1

   


class FacultySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id','name','modules')
        depth=1
    

class FileSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField()
    module_id = serializers.IntegerField()
    class Meta:
        model = File
        fields='__all__'


    def get_module(self,obj):
        data = {"id":obj.module.id,"name":obj.module.name} 
        return data


    def create(self,validated_data,**kwargs):
        module_id = validated_data.get("module_id")  
        module = get_object_or_404(Module,id=module_id)
        file = File.objects.create(**validated_data,module=module)
        return file


