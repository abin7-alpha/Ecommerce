import sys, traceback

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status as Status

from account.models import Retailer, Device, RetailerDevice

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def save_user_device_details(request):
	output = {}
	data = request.data
	try:
		retailer_id = data['retailerId']
		device_id = data["deviceId"]
		device_platform = data["devicePlatform"]
		device_manufacturer = data["deviceManufacturer"]
		device_model = data["deviceModel"]
		device_os_version = data["deviceOsVersion"]
		language = data['language']
		fcm_token = data['fcmToken']
		try:
			retailer = Retailer.objects.get(id=retailer_id)
			try:
				try:
					device = Device.objects.get(device_id=device_id)
					device.device_platform=device_platform
					device.device_model=device_model
					device.device_manufacturer=device_manufacturer
					device.device_os_version=device_os_version
					device.language=language
					device.save()
				except:
					device = Device.objects.create(
                        device_id=device_id,
                        device_platform=device_platform,
                        device_model=device_model,
                        device_manufacturer=device_manufacturer,
                        device_os_version=device_os_version,
                        language=language
                    )
				try:
					retailer_device = RetailerDevice.objects.get(retailer=retailer, device=device)
					retailer_device.fcm_token = fcm_token
					retailer_device.save()
				except:
					retailer_device = RetailerDevice.objects.create(
                        retailer=retailer,
                        device=device,
                        fcm_token=fcm_token
                    )
					
				output['status'] = 'success'
				output['status_text'] = 'successfully saved the user device details'
				status = Status.HTTP_200_OK
			except:
				traceback.print_exc(file=sys.stdout)
				output['status'] = 'failed'
				output['status_text'] = 'Failed to save the user details'
				status = Status.HTTP_400_BAD_REQUEST
		except:
			traceback.print_exc(file=sys.stdout)
			output['status'] = 'failed'
			output['status_text'] = 'Invalid Retailer'
			status = Status.HTTP_400_BAD_REQUEST
	except KeyError as e:
		traceback.print_exc(file=sys.stdout)
		output['status'] = 'failed'
		output['status_text'] = f'Invalid data,{e} key error'
		status = Status.HTTP_400_BAD_REQUEST
	
	return Response(output, status=status)