from django.db import models
# Create your models here.



#file types
TYPES = {"Lesson":"cour","TD":"td","Exam":"exam"}



class Module(models.Model):
    name = models.CharField(max_length=50,null=False)
    short = models.CharField(max_length=10,null=False,blank=False)
    drive_id = models.CharField(max_length=100,null=True,blank=True)
    semester = models.CharField(max_length=100,null=False)
    @property
    def file_count(self):
        count = 0;
        for file in self.files:
            count +=1


    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    modules = models.ManyToManyField(Module)
    short = models.CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        return self.name

class File(models.Model):
    accepted = models.BooleanField(default=False)
    file = models.FileField(upload_to="files",blank=True,null=True)
    drive_link = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(null=False)
    title = models.CharField(max_length=100,null=False)
    downloads_count = models.IntegerField(default=0)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    file_type = models.CharField(max_length=20,choices=TYPES,null=False,blank=False)   
    
    @property
    def file_name(self):
        name = str(self.file.name).replace("files/","")
        return name
 
    @property
    def file_size(self):
        bytes_size = self.file.size
        if bytes_size > 1000:
            return str(bytes_size/1000) + " KB"

        elif bytes_size > 1000 * 1000:
            return str(bytes_size/(1000*1000) + " MB")
        
    
    @property
    def file_extention(self)-> str:
        _,extention = str(self.file.name).split(".")
        return extention



    def __str__(self):
        return self.title
