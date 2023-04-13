from rest_framework.response import Response
from rest_framework import status

from account.models import Staff

# def super_admin_test(user_id):
#     flag = False
#     staff = Staff.objects.get(id=user_id)
#     if staff.is_super_admin and staff.is_logistics_manager and staff.is_order_manager and staff.is_payments_manager and staff.is_retailer_manager:
#         flag = True
#     return flag

def logistics_manager_test(user_id):
    flag = False
    staff = Staff.objects.get(id=user_id)
    if staff.is_logistics_manager or staff.is_super_admin:
        flag = True
    return flag

def order_manager_test(user_id):
    flag = False
    staff = Staff.objects.get(id=user_id)
    if staff.is_order_manager or staff.is_super_admin:
        flag = True
    return flag

def payment_manager_test(user_id):
    flag = False
    staff = Staff.objects.get(id=user_id)
    if staff.is_payments_manager or staff.is_super_admin:
        flag = True
    return flag

def retailer_manager_test(user_id):
    flag = False
    staff = Staff.objects.get(id=user_id)
    if staff.is_retailer_manager or staff.is_super_admin:
        flag = True
    return flag

# def is_admin(methods=[], err_message="Admin authorization required."):
#     def decorator(view_function):
#         def decorated_function(request, *args, **kwargs):
#             if not 'Authorization' in request.headers:
#                 print(request.headers['Authorization'])
#                 return Response({"detail": err_message}, status=status.HTTP_401_UNAUTHORIZED)
            
#             if not super_admin_test(request.headers['user_id']):
#                 return Response({"status": "failed", "status_text": "You dont have the permission to access this"}, status=status.HTTP_401_UNAUTHORIZED)
            
#             return view_function(request, *args, **kwargs)
#         return decorated_function
#     return decorator

def is_logistics_manager(methods=[], err_message="Admin authorization required."):
    def decorator(view_function):
        def decorated_function(request, *args, **kwargs):
            if not 'Authorization' in request.headers:
                print(request.headers['Authorization'])
                return Response({"detail": err_message}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                user_id = request.data['userid']
            except:
                user_id = request.query_params.get('userid')

            if not logistics_manager_test(user_id):
                return Response({"status": "Unauthorized", "status_text": "You dont have the permission to access this"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return view_function(request, *args, **kwargs)
        return decorated_function
    return decorator

def is_payment_manager(methods=[], err_message="Admin authorization required."):
    def decorator(view_function):
        def decorated_function(request, *args, **kwargs):
            if not 'Authorization' in request.headers:
                print(request.headers['Authorization'])
                return Response({"detail": err_message}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                user_id = request.data['userid']
            except:
                user_id = request.query_params.get('userid')

            if not payment_manager_test(user_id):
                return Response({"status": "Unauthorized", "status_text": "You dont have the permission to access this"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return view_function(request, *args, **kwargs)
        return decorated_function
    return decorator

def is_order_manager(methods=[], err_message="Admin authorization required."):
    def decorator(view_function):
        def decorated_function(request, *args, **kwargs):
            if not 'Authorization' in request.headers:
                print(request.headers['Authorization'])
                return Response({"detail": err_message}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                user_id = request.data['userid']
            except:
                user_id = request.query_params.get('userid')
            
            if not order_manager_test(user_id):
                return Response({"status": "Unauthorized", "status_text": "You dont have the permission to access this"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return view_function(request, *args, **kwargs)
        return decorated_function
    return decorator

def is_retailer_manager(methods=[], err_message="Admin authorization required."):
    def decorator(view_function):
        def decorated_function(request, *args, **kwargs):
            if not 'Authorization' in request.headers:
                print(request.headers['Authorization'])
                return Response({"detail": err_message}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                user_id = request.data['userid']
            except:
                user_id = request.query_params.get('userid')
            
            if not retailer_manager_test(user_id):
                return Response({"status": "Unauthorized", "status_text": "You dont have the permission to access this"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return view_function(request, *args, **kwargs)
        return decorated_function
    return decorator
