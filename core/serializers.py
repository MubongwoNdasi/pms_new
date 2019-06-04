# import rest_auth
# from rest_auth.utils import import_callable
# from rest_framework import serializers
# from core.models import Drug, Category, User
#
# from django.contrib.auth import get_user_model, authenticate
# from rest_framework.authtoken.models import Token
# from rest_framework import serializers, exceptions
# from rest_framework.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
# from django.conf import settings
# from rest_auth.serializers import LoginSerializer as Login, UserDetailsSerializer
# from rest_auth.registration.serializers import RegisterSerializer
#
# from allauth.account import app_settings as allauth_settings
# from allauth.utils import (email_address_exists, get_username_max_length)
# from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email
#
#
# class DrugSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Drug
#         fields = '__all__'
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['name']
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', 'password', 'is_admin']
#
#
# class CustomRegisterSerializer(RegisterSerializer):
#     first_name = serializers.CharField(max_length=100)
#     last_name = serializers.CharField(max_length=100)
#     address = serializers.CharField(max_length=300, help_text='enter address')
#     tel = serializers.CharField(max_length=13, help_text='telephone number')
#
#     is_admin = serializers.BooleanField(default=False)
#
#     class Meta:
#         model = User
#         fields = ['email', 'first_name', 'last_name', 'password', 'address', 'tel', 'is_admin']
#
#     def get_cleaned_data(self):
#         return {
#             'first_name': self.validated_data.get('first_name', ''),
#             'last_name': self.validated_data.get('last_name', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'password2': self.validated_data.get('password2', ''),
#             'email': self.validated_data.get('email', ''),
#             'address': self.validated_data.get('address', ''),
#             'tel': self.validated_data.get('tel', ''),
#         }
#
#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.is_admin = self.cleaned_data.get('is_admin')
#         user.address = self.cleaned_data.get('address')
#         user.tel = self.cleaned_data.get('tel')
#         user.save()
#         adapter.save_user(request, user, self)
#         return user
#
#
# class LoginSerializer(Login):
#     # username = serializers.CharField(required=False, allow_blank=True)
#     email = serializers.EmailField(required=True, allow_blank=False)
#     password = serializers.CharField(style={'input_type': 'password'})
#
#     def authenticate(self, **kwargs):
#         return authenticate(self.context['request'], **kwargs)
#
#     def get_fields(self):
#         fields = super(LoginSerializer, self).get_fields()
#         fields['email'] = fields['username']
#         del fields['username']
#         return fields
#
#     def _validate_email(self, email, password):
#         user = None
#
#         if email and password:
#             user = self.authenticate(email=email, password=password)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise exceptions.ValidationError(msg)
#
#         return user
#
#     def validate(self, attrs):
#         # username = attrs.get('username')
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         user = None
#
#         if 'allauth' in settings.INSTALLED_APPS:
#             from allauth.account import app_settings
#
#             # Authentication through email
#             if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
#                 user = self._validate_email(email, password)
#
#         attrs['user'] = user
#         return attrs
#
#
# class TokenSerializer(serializers.ModelSerializer):
#     user_type = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Token
#         fields = ['key', 'user', 'user_type']
#
#     def get_user_type(self, obj):
#         serializer_data = UserSerializer(obj.user).data
#         is_admin = serializer_data.get('is_admin')
#         return {
#             'is_admin': is_admin,
#         }
#
#
#
# # class RegisterSerializer(serializers.Serializer):
# #     # username = serializers.CharField(
# #     #     max_length=get_username_max_length(),
# #     #     min_length=allauth_settings.USERNAME_MIN_LENGTH,
# #     #     required=allauth_settings.USERNAME_REQUIRED
# #     # )
# #     email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
# #     first_name = serializers.CharField(max_length=100)
# #     last_name = serializers.CharField(max_length=100)
# #     address = serializers.CharField(max_length=300, help_text='enter address')
# #     password1 = serializers.CharField(write_only=True)
# #     password2 = serializers.CharField(write_only=True)
# #
# #     def validate_username(self, username):
# #         username = get_adapter().clean_username(username)
# #         return username
# #
# #     def validate_email(self, email):
# #         email = get_adapter().clean_email(email)
# #         if allauth_settings.UNIQUE_EMAIL:
# #             if email and email_address_exists(email):
# #                 raise serializers.ValidationError(
# #                     _("A user is already registered with this e-mail address."))
# #         return email
# #
# #     def validate_password1(self, password):
# #         return get_adapter().clean_password(password)
# #
# #     def validate(self, data):
# #         if data['password1'] != data['password2']:
# #             raise serializers.ValidationError(_("The two password fields didn't match."))
# #         return data
# #
# #     def custom_signup(self, request, user):
# #         pass
# #
# #     def get_cleaned_data(self):
# #         return {
# #             'username': self.validated_data.get('username', ''),
# #             'password1': self.validated_data.get('password1', ''),
# #             'email': self.validated_data.get('email', '')
# #         }
# #
# #     def save(self, request):
# #         adapter = get_adapter()
# #         user = adapter.new_user(request)
# #         self.cleaned_data = self.get_cleaned_data()
# #         adapter.save_user(request, user, self)
# #         self.custom_signup(request, user)
# #         setup_user_email(request, user, [])
# #         return user
#
#
#
# class RegisteringSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     address = serializers.CharField(required=True)
#     phone = serializers.CharField(max_length=15)
#
#     # user_type = serializers.ChoiceField(
#     # choices=(('Farmer', 'Farmer'),('Windmill owner', 'Windmill owner'),('Solar panel owner', 'Solar panel owner'),),
#     # style={'base_template': 'radio.html'},
#     # required=True, write_only=True)
#
#
#     password1 = serializers.CharField(required=True, write_only=True)
#     password2 = serializers.CharField(required=True, write_only=True)
#
#     is_admin = serializers.BooleanField(default=False)
#
#     def validate_email(self, email):
#         email = get_adapter().clean_email(email)
#         if allauth_settings.UNIQUE_EMAIL:
#             if email and email_address_exists(email):
#                 raise serializers.ValidationError(
#                     _("A user is already registered with this e-mail address."))
#         return email
#
#     def validate_password1(self, password):
#         return get_adapter().clean_password(password)
#
#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError(
#                 _("The two password fields didn't match."))
#         return data
#
#     def get_cleaned_data(self):
#         return {
#             'first_name': self.validated_data.get('first_name', ''),
#             'last_name': self.validated_data.get('last_name', ''),
#             'address': self.validated_data.get('address', ''),
#             'phone': self.validated_data.get('phone', ''),
#             'user_type': self.validated_data.get('user_type', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'email': self.validated_data.get('email', ''),
#             'is_admin': self.validated_data.get('is_admin', ''),
#         }
#
#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
#         setup_user_email(request, user, [])
#
#         user.address = self.cleaned_data.get('address')
#         # user.user_type = self.cleaned_data.get('user_type')
#         user.phone = self.cleaned_data.get('phone')
#         user.is_admin = self.cleaned_data.get('is_admin')
#
#         user.save()
#         return user
#
