from django.urls import path
from .views import get_faculty,get_faculties,module,search_files,upload_file,download_file

urlpatterns = [
            path("faculty/",get_faculty,name="faculty"),
            path("faculties/",get_faculties,name="faculties"),
        
            path("module/",module,name="module"),
            path("search/",search_files,name="search"),
            path("upload/",upload_file,name="upload-file"),
            path("download/<int:id>",download_file,name="download"),
        ]
