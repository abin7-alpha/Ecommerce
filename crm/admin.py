from django.contrib import admin

from crm.models import RequestType, UserType, ServiceRequest, RetailerServiceRequest

admin.site.register(RequestType)
admin.site.register(UserType)
admin.site.register(ServiceRequest)
admin.site.register(RetailerServiceRequest)

