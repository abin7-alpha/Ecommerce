from django.db import models

class Image(models.Model):
	img_key=models.CharField(null=True,max_length=2048)
	updated = models.DateTimeField(auto_now=True)

class File(models.Model):
    file=models.FileField(upload_to='documents/', null=True, blank=False,max_length=None)
    fileUse=models.CharField(null=True,max_length=200,default="Expense")
    updated=models.DateTimeField(auto_now=True)


class WebFile(models.Model):
    file_url= models.CharField(null=True,max_length=512)
    fileUse = models.CharField(null=True,max_length=200,default="Expense")
    updated = models.DateTimeField(auto_now=True)
