from django.urls import path
from .views import get_faculty,get_faculties, get_faculty_byID, get_file_byID,module,search_files,upload_file,download_file

urlpatterns = [
            path("fac/<int:id>",get_faculty_byID,name="single faculty"),
            path("fac/all",get_faculties,name="all faculties"),
            path("module/<int:id>",get_faculty_byID,name='mod-id'),
            path("file/<int:id>",get_file_byID,name='fac-id'), 
            path("fac-search/",get_faculty,name='fac-search'), 
            path("search-module/",module,name="get module"),
            path("search-file/",search_files,name="search-file"),
            path("upload/",upload_file,name="upload-file"),
            path("download/<int:id>",download_file,name="download-file"),
        ]
