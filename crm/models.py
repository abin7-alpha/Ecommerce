from django.db import models
from account.models import Retailer

class RequestType(models.Model):
    request_type = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.request_type
    
class UserType(models.Model):
    user_type = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_type + str(self.id)
    
class QueryLog(models.Model):
    log = models.TextField(null=False, blank=False, max_length=500)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

class ServiceRequest(models.Model):
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, default='guest')
    request_type = models.ForeignKey(RequestType, on_delete=models.CASCADE, null=False, blank=False, default='other')
    query_log = models.ManyToManyField(QueryLog)
    name = models.CharField(max_length=100, blank=False, null=True)
    email = models.CharField(max_length=100, blank=False, null=True)
    phone_no = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=1000, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + str(self.id)

class RetailerServiceRequest(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
