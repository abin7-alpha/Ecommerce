from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

from geoposition.fields import GeopositionField

from janaushadi import settings
from office.models import DistributionCenter, City
from commodity.models import DcCommodity

from datetime import datetime
from pytz import timezone

USER_TYPE= (('Retailer', 'Retailer'), ('Staff', 'Staff'))

GENDER_TYPE= (('Male','Male'), ('Female','Female'))

class BasicUser(models.Model):
	django_user = models.ForeignKey(User, null=False, related_name='django_user', on_delete=models.CASCADE)
	name = models.CharField(null=False, max_length=50)
	email = models.CharField(null=True, max_length=100, db_index=False, unique=False)
	phone = models.CharField(null=False, max_length=20, db_index=True, unique=True)
	secondary_phone = models.CharField(null=True, max_length=20)
	passcode = models.CharField(null=False, max_length=20)
	gender = models.CharField(null=False, max_length=20, default='Male', choices=GENDER_TYPE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	user_type = models.CharField(null=False, max_length=100, default='Retailer', choices=USER_TYPE)
	id_proof_url = models.CharField(max_length=2048, null=True, blank=True)
	profile_pic = models.CharField(max_length=2048, null=True, blank=True, default=settings.DEFAULT_PROFILE_IMAGE)
	is_active = models.BooleanField(default=False)
	is_email_verified = models.BooleanField(default=False)
	is_phone_verified = models.BooleanField(default=False)  
	last_logged_in = models.DateTimeField(auto_now=True)
	otp = models.CharField(null=True, blank=True, max_length=10)
	otp_creation_time = models.DateTimeField(null=True, blank=True)
	mobile_verify_otp = models.CharField(null=True, blank=True, max_length=10)

	def __str__(self):
		return str(self.name)+" "+str(self.phone)

class AddressType(models.Model):
	name = models.CharField(null=False, max_length=512)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return str(self.name)
	
class Addresses(models.Model):
	line1 = models.CharField(null=False, blank=False, max_length=512)
	line2 = models.CharField(null=True, blank=True, max_length=512)
	line3 = models.CharField(null=True, blank=True, max_length=512)
	city = models.CharField(null=False, max_length=30)
	state = models.CharField(null=True, max_length=50)
	country = models.CharField(null=False, max_length=20)
	zipcode = models.CharField(null=False, max_length=10)
	geoposition = GeopositionField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	address_type = models.ForeignKey(AddressType, null=False, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.line1)+" "+str(self.city)+" "+str(self.country)

class RetailerShop(models.Model):
	shop_address = models.ForeignKey(Addresses, null=True, blank=True, on_delete=models.SET_NULL)
	shop_code = models.CharField(null=True, max_length=10)
	shop_name = models.CharField(null=False, blank=False, max_length=1024)
	shop_phone = models.CharField(null=False, max_length=20,db_index=False)
	position = GeopositionField()
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	shop_pic_in = models.CharField(max_length=650, null=True, blank=True)
	shop_pic_out = models.CharField(max_length=650, null=True, blank=True)
	dc = models.ForeignKey(DistributionCenter, null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return str(self.shop_name)+" : "+str(self.id)

LANGUAGE_CHOICES = (("ગુજરાતી", 'gu'), ("বাংলা", 'bn'), ("తెలుగు", 'te'), ("தமிழ்", 'ta'), ("मराठी", 'mr'), ("हिन्दी", 'hi'), ('English', 'en'), ("മലയാളം", 'ml'))
# LANGUAGE_CHOICES = (('gu', "ગુજરાતી"), ('bn', "বাংলা"), ('te', "తెలుగు"), ('ta', "தமிழ்"), ('mr', "मराठी"), ('hi', "हिन्दी"), ('en', 'English'))

class Retailer(models.Model):
	user = models.ForeignKey(BasicUser, null=False, on_delete=models.PROTECT)
	address = models.ForeignKey(Addresses, null=True, blank=True, on_delete=models.SET_NULL)
	shops = models.ManyToManyField(RetailerShop, related_name="retailer", blank=True)
	dc = models.ForeignKey(DistributionCenter, null=True, blank=True, on_delete=models.SET_NULL)
	selected_city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
	# shop_name = models.CharField(null=False, blank=False, max_length=1024)
	position = GeopositionField(blank=True, null=True)
	gst_no = models.CharField(null=True, max_length=50, blank=True)
	# address = models.CharField(null=True, max_length=1024, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	is_admin_verified = models.BooleanField(default=False)
	is_payment_check_required = models.BooleanField(default=False)
	pending_amount_limit = models.FloatField(null=True, blank=True)
	total_amount_outstanding = models.FloatField(null=True, blank=True, default=0)
	updated = models.DateTimeField(auto_now=True)
	shop_pic_in = models.CharField(max_length=1024, null=True, blank=True)
	shop_pic_out = models.CharField(max_length=1024, null=True, blank=True)
	document_pic = models.CharField(max_length=1024, null=True, blank=True)
	city = models.CharField(max_length=650, null=True, blank=True)
	prefered_lang = models.CharField(choices=LANGUAGE_CHOICES, max_length=10, null=False, default='English')
	# lastActiveLogin
	last_active_login = models.DateTimeField(null=True, blank=True)
	last_notification_view = models.DateTimeField(null=True, blank=True, auto_now_add=True)
	# lastNotificationView

	def __str__(self):
		return str(self.user.name)
	
	@property
	def prefered_lang_code(self):
		return self.get_prefered_lang_display()
	
	@property
	def orders(self):
		return self.order_set.all()

class DistributionCenterManager(models.Model):
	user = models.ForeignKey(BasicUser, null=False, on_delete=models.PROTECT)
	is_active = models.BooleanField(default=True)
	dcs = models.ManyToManyField(DistributionCenter, related_name="dcs")

	def __str__(self):
		return str(self.user.name)+" : "+str(self.user.phone)

current_date_time = timezone('Asia/Kolkata').localize(datetime.now())
class Staff(models.Model):
	user = models.ForeignKey(BasicUser, null=True, on_delete=models.PROTECT, blank=True)
	name = models.CharField(null=False, max_length=1024)
	email = models.CharField(null=True, max_length=100, db_index=False, unique=True)
	phone = models.CharField(null=False, max_length=20, db_index=True, unique=True)
	passcode = models.CharField(null=False, max_length=20)
	gender = models.CharField(null=False, max_length=20, default='Male', choices=GENDER_TYPE)
	is_active = models.BooleanField(default=True)
	user_type = models.CharField(null=False, max_length=100, default='staff', choices=USER_TYPE)
	id_proof_url = models.CharField(max_length=650, null=True, blank=True)
	profile_pic = models.CharField(max_length=650, null=True, blank=True)
	dcs = models.ManyToManyField(DistributionCenter)
	# ccs = models.ManyToManyField(CollectionCenter)
	is_logistics_manager = models.BooleanField(default=False)
	is_order_manager = models.BooleanField(default=False)
	is_payments_manager =  models.BooleanField(default=False)
	is_super_admin = models.BooleanField(default=False)
	is_retailer_manager = models.BooleanField(default=False)
	last_stock_notified = models.DateTimeField(null=True, blank=True)
	last_logged_in = models.DateTimeField(auto_now=True)
	otp = models.CharField(null=True, blank=True, max_length=10)
	otp_creation_time = models.DateTimeField(null=True, blank=True)

	def save(self, *args, **kwargs):
        # Provider Id appended
		isNewRecord = False
		if self.id == None:
			isNewRecord = True
		super(Staff, self).save(*args, **kwargs)
		
		if isNewRecord:
			user = User.objects.create(username=self.name, email=self.email)
			user.set_password(self.passcode)
			user.save()

			basic_user = BasicUser.objects.create(
					django_user=user,
					name=self.name,
					email=self.email,
					phone=self.phone,
					gender=self.gender,
					user_type=self.user_type,
					passcode=self.passcode
			)
			
			self.user = basic_user
			self.save()

			return basic_user

	def __str__(self):
		return str(self.name)+" : "+str(self.phone)

class City(models.Model):
	name = models.CharField(null=False, max_length=150)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return str(self.name)

class Banks(models.Model):
	bank_name = models.CharField(null=False, max_length=30)
	account_number = models.CharField(null=False, max_length=20)
	ifsc_code = models.CharField(null=False, max_length=20)
	account_holder_name = models.CharField(null=False, max_length=1024)
	pass_book_image = models.CharField(max_length=1024, null=True, blank=True)
	pancard_image = models.CharField(max_length=2048, null=True, blank=True)
	is_verified = models.BooleanField(null=False, default=False)
	is_active = models.BooleanField(null=False, default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return str(self.account_holder_name)+" : "+str(self.bank_name)

class DistributionManagerloggedInData(models.Model):
	store_manager = models.ForeignKey(DistributionCenterManager, null=False, on_delete=models.PROTECT)
	logged_in_location = GeopositionField()
	logged_in_address = models.CharField(null=True, max_length=1024, blank=True)
	logged_in_device = models.CharField(null=True, max_length=1024, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

APP_NAMES= (('Captains_App', 'Captains_App'), ('Retailer_App', 'Retailer_App'), 
            ('Retailer_Web', 'Retailer_Web'), ('Retailer_Mail', 'Retailer_Mail'))

class NotificationType(models.Model):
	name = models.CharField(max_length=50, null=False)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	
class RetailerNotification(models.Model):
	retailer = models.ForeignKey(Retailer, null=False, on_delete=models.CASCADE)
	title = models.CharField(null=False,max_length=150)
	subtitle = models.CharField(null=True,max_length=150)
	notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE, null=True, blank=True)
	content = models.CharField(null=True,max_length=1024)	
	image_url = models.CharField(max_length=650, null=True,blank=True)
	app_name = models.CharField(max_length=100, choices=APP_NAMES, null=True)
	is_in_kannada = models.BooleanField(null=False, default=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.retailer.user.name + f' {self.id}' 

class RetailerCommodityRequests(models.Model):
	dc_commodity = models.ForeignKey(DcCommodity, on_delete=models.CASCADE, null=False)
	retailer = models.ForeignKey(Retailer, null=False, on_delete=models.CASCADE)
	subscribed_on = models.DateTimeField(auto_now_add=True)
	# status = 
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	no_of_times_notified = models.IntegerField(default=0)
	availabilty_last_notified = models.DateField(null=True)
	# DcCommodity, Retailer, subscribedOn, status, isActive,isDeleted, 
	# created,updated, availabilityLastNotified

	def dcCommodity(self):
		return self.dc_commodity

	def __str__(self):
		return self.dc_commodity.commodity.name

class CommodityRequestNotifications(models.Model):
	retailer_notification = models.ForeignKey(RetailerNotification, on_delete=models.CASCADE)
	retailer_commodity_requests = models.ForeignKey(RetailerCommodityRequests, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	is_viewed_by_retailer = models.BooleanField(default=False)
	# RetailerNotification, RetailerCommodityRequests, created, isViewedByRetailer

class RetailerRecentSearch(models.Model):
	dc_commodity = models.ForeignKey(DcCommodity, on_delete=models.CASCADE, null=False)
	retailer = models.ForeignKey(Retailer, null=False, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.dc_commodity.commodity.name
	
DEVICE_TYPES=(('1', 'ANDROID'), ('0', 'iOS'), ('2', 'AMAZON'), ('3', 'WINDOWS'),
              ('5', 'CHROME_WEB_PUSH'))

# class RetailerDevice(models.Model):
# 	retailer = models.ForeignKey(Retailer, null=False, on_delete=models.CASCADE)
# 	device_id = models.CharField(null=False, max_length=1024)
# 	player_id = models.CharField(null=False, max_length=1024)
# 	device_platform = models.CharField(max_length=100, choices=DEVICE_TYPES, null=False)
# 	device_manufacturer = models.CharField(max_length=100, null=True)
# 	device_model = models.CharField(max_length=100, null=True)
# 	device_os_version = models.CharField(max_length=100, null=True)
	# language = models.CharField(max_length=10, default='en')
# 	is_active = models.BooleanField(default=True)
	
class Device(models.Model):
    device_id = models.CharField(null=False, max_length=2048)
    # playerId=models.CharField(null=False,max_length=2048)
    device_platform = models.CharField(max_length=100, choices=DEVICE_TYPES, null=False)
    device_manufacturer = models.CharField(max_length=100, null=True)
    device_model = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=10, default='English')
    device_os_version = models.CharField(max_length=100, null=True)
    
class RetailerDevice(models.Model):
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.DO_NOTHING)
    retailer = models.ForeignKey(Retailer, null=False, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    fcm_token = models.CharField(null=True, max_length=2048)
    
class StaffDevice(models.Model):
    device = models.ForeignKey(Device, null=False, blank=False, on_delete=models.DO_NOTHING)
    staff = models.ForeignKey(Staff, null=False, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    fcm_token = models.CharField(null=True, max_length=2048)
	