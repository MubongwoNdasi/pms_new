# from allauth.account.forms import SetPasswordField, PasswordField
from django import forms
from core.models import User, Profile, Pharmacy

# from phonenumber_field.modelfields import PhoneNumberField
# from django.utils.translation import ugettext_lazy as _


class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "input_text", }), required=True,)
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "input_text", }), required=True,)
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "input_text", }), required=False)
    address = forms.CharField(max_length=100)
    phone = forms.CharField(help_text="Number must be in international format", label="Phone Number", max_length=30, widget=forms.TextInput(attrs={"class": "input_text", }))

    class Meta:
        model = User

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data['address']
        user.phone = self.cleaned_data['phone']
        user.save()


class UserProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'address']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class PharmacyCreateForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = '__all__'
