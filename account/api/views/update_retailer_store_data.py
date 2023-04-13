import sys, traceback

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status as Status

from account.models import Retailer, RetailerShop, Addresses

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def update_retaielr_store_data(request):
	output = {}
	data = request.data
	try:
		retailer_id = data['retailerId']
		shop_id = data['shopId']
		shop_name = data['shopName']
		shop_phone = data['shopPhone']
		shop_address_line_one = data['shopAddressLineOne']
		shop_address_line_two = data['shopAddressLineTwo']
		shop_address_line_three = data['shopAddressLineThree']
		city = data['city']
		zipcode = data['zipcode']
		try:
			retailer = Retailer.objects.get(id=retailer_id)
			shop = RetailerShop.objects.get(id=shop_id)
			# addresses, created = Addresses.objects.get_or_create()
			try:
				shop.shop_name = shop_name
				shop.shop_phone = shop_phone
				shop.shop_address.line1 = shop_address_line_one
				shop.shop_address.line2 = shop_address_line_two
				shop.shop_address.line3 = shop_address_line_three
				shop.shop_address.city = city
				shop.shop_address.zipcode = zipcode
				shop.shop_address.save()
				shop.save()
				output['status'] = 'success'
				output['status_text'] = 'successfully updated the retailer data'
				status = Status.HTTP_200_OK
			except:
				traceback.print_exc(file=sys.stdout)
				output['status'] = 'failed'
				output['status_text'] = 'Failed to update the retailer store data'
				status = Status.HTTP_304_NOT_MODIFIED
		except:
			traceback.print_exc(file=sys.stdout)
			output['status'] = 'failed'
			output['status_text'] = 'Invalid Retailer'
			status = Status.HTTP_404_NOT_FOUND
	except:
		traceback.print_exc(file=sys.stdout)
		output['status'] = 'failed'
		output['status_text'] = 'Invalid data, key error'
		status = Status.HTTP_400_BAD_REQUEST
	
	return Response(output, status=status)