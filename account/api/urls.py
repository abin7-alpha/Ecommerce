from django.urls import path
from account.api.views.retailer_registration_view import register_retailer
from account.api.views.login_view import login_user
from account.api.views.logout_view import logout_user
from account.api.views.get_retailer_details import get_retailer_details
from account.api.views.retailer_prefered_language import update_retailer_prefered_language
from account.api.views.verify_email_view import verify_user_email
from account.api.views.resend_user_verification_email import resend_user_verification_mail
from account.api.views.reset_user_password import request_new_password, reset_password_request, change_user_password_console
from account.api.views.reset_user_password import change_user_password_forgot
from account.api.views.get_dashboard_data import get_dashboard_data
from account.api.views.register_email_sandbox import register_email_to_sandbox
from account.api.views.register_phone_number_topic import register_phone_number_to_topic, verify_sanbox_number
from account.api.views.send_sms import send_SMS
from account.api.views.generate_otp_retailer import generate_otp_for_retailer_edit
from account.api.views.generate_otp_for_forgot_password import generate_otp_for_forgot_password
from account.api.views.verify_otp_for_retailer import verify_otp_for_retailer
from account.api.views.verify_otp_for_forgot import verify_otp_for_retailer_forgot
from account.api.views.get_access_token_using_refresh import get_access_using_refresh_token
from account.api.views.notification_api import notify_user
from account.api.views.get_retailer_notificaitons import get_retailer_notifications
from account.api.views.get_all_retailers import get_all_retailers
from account.api.views.admin_login import login_admin
from account.api.views.admin.register_retailer_by_admin import register_retailer_by_admin
from account.api.views.update_retailer_data import update_user_data
from account.api.views.update_retailer_store_data import update_retaielr_store_data
from account.api.views.get_retailer_notification_length import get_retailer_notification_count
from account.api.views.record_notified_date import record_notification_view_date
from account.api.views.save_user_device_details import save_user_device_details

from account.api.views.admin.assign_dc import assign_dc_for_retailer
from account.api.views.admin.sent_notification_to_retailer import send_notification_to_retailer
from account.api.views.admin.set_is_payment_required_true import set_is_payment_required_true
from account.api.views.admin.approve_or_block_retailer import approve_or_block_retailer
from account.api.views.add_to_recent_search import add_to_recent_searches
from account.api.views.get_retailer_recent_search import get_retailer_recent_searches
from account.api.views.admin.create_new_retailer_shop import create_new_retailer_shop
from account.api.views.admin.update_retailer_shop_details import update_retailer_shop
from account.api.views.admin.generate_otp_for_retailer_edit_admin import generate_otp_for_retailer_edit_by_admin
from account.api.views.admin.generate_otp_for_retailer_password_admin import generate_otp_for_retailer_forgot_password_by_admin
from account.api.views.admin.change_retailer_password_by_admin import verify_otp_and_change_user_password
from account.api.views.admin.retailer_edit_by_admin import retailer_edit_by_admin
from account.api.views.admin.activate_or_deactivate_retailer_shop import activate_or_deactivate_shop

urlpatterns = [
    path('register-retailer', register_retailer, name='register_retailer'),
    path('verify-user-email', verify_user_email, name='verify-user-email'),
    path('resend-verify-user-email', resend_user_verification_mail, name='resend_user_verification_email'),
    path('login-user', login_user, name='login_user'),
    path('get-access-token-using-refresh-token', get_access_using_refresh_token, name='get_access_using_refresh_token'),
    # path('logout-user', logout_user, name='logout_user'),
    # path('csrf-cookie', GetCSRFToken.as_view()),
    path('get-retailer-details', get_retailer_details, name='get_retailer_details'),
    path('get-retailer-notifications', get_retailer_notifications, name='get_retailer_notifications'),
    path('change-prefered-language', update_retailer_prefered_language, name='update_retailer_prefered_language'),
    path('request-new-password', request_new_password, name='request_new_password'),
    path('reset-password-request', reset_password_request, name='reset_password_request'),
    path('change-user-password-console', change_user_password_console, name='change_user_password_console'),
    path('change-user-password-forgot', change_user_password_forgot, name='change_user_password_forgot'),
    path('get-dashboard-data', get_dashboard_data, name='get_dashboard_data'),
    path('generate-otp-for-retailer-edit', generate_otp_for_retailer_edit, name='generate_otp_for_retailer_edit'),
    path('generate-otp-for-forgot-password', generate_otp_for_forgot_password, name='generate_otp_for_forgot_password'),
    path('verify-otp-for-retailer', verify_otp_for_retailer, name='verify_otp_for_retailer'),
    path('verify-otp-for-forgot-retailer', verify_otp_for_retailer_forgot, name='verify_otp_for_forgot-retailer'),
    path('register-email-to-sandbox', register_email_to_sandbox, name='register_email_to_sandbox'),
    path('register-phone-number-to-topic', register_phone_number_to_topic, name='register_phone_number_to_topic'),
    path('register-phone-number-to-topic', register_phone_number_to_topic, name='register_phone_number_to_topic'),
    path('verify-sandbox-number', verify_sanbox_number, name='verify_sandbox_number'),
    path('update-retailer-data', update_user_data, name='update_user_data'),
    path('update-retailer-store-data', update_retaielr_store_data, name='update_retailer_store_data'),
    path('get-retailer-notification-count', get_retailer_notification_count, name='get_retailer_notification_count'),
    path('record-notification-view-date', record_notification_view_date, name='record_notification_view_date'),
    path('save-user-device-details', save_user_device_details, name='save_user_device_details'),

    path('send-sms', send_SMS, name='send_sms'),
    path('notify-user', notify_user, name='notify_user'),

    path('login-admin', login_admin, name='login_admin'),
    path('get-all-retailers', get_all_retailers, name='get_all_retailers'),
    path('register-retailer-by-admin', register_retailer_by_admin, name='register_retailer_by_admin'),
    path('set-is-payment-check-required', set_is_payment_required_true, name='set_is_payment_check_required'),
    path('approve-or-block-retailer', approve_or_block_retailer, name='approve_or_block_retailer'),
    path('assign-dc-for-retailer', assign_dc_for_retailer, name='assign_dc_for_retailer'),
    path('send-notification-to-retailer', send_notification_to_retailer, name='send_notification_to_retailer'),
    path('add-to-recent-searches', add_to_recent_searches, name='add_to_recent_searches'),
    path('get-retailer-recent-searches', get_retailer_recent_searches, name='get_retailer_recent_searches'),
    path('create-new-retailer-shop', create_new_retailer_shop, name='create_new_retailer_store'),
    path('update-retailer-shop', update_retailer_shop, name='update_retailer_shop'),
    path('generate-otp-for-retailer-reset-password-by-admin', generate_otp_for_retailer_forgot_password_by_admin, name='generate_otp_for_reset_password_by_admin'),
    path('generate-otp-for-retailer-edit-by-admin', generate_otp_for_retailer_edit_by_admin, name='generate_otp_for_retailer_edit_by_admin'),
    path('verify-otp-and-change-user-password-by-admin', verify_otp_and_change_user_password, name='verify_otp_and_change_user_password'),
    path('retailer-edit-by-admin', retailer_edit_by_admin, name='retailer_edit_by_admin'),
    path('activate-or-deactivate-shop', activate_or_deactivate_shop, name='activate_or_deactivate_shop'),
]
