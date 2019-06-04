from drug.models import Drugs, Category
from django import forms
from django.utils import timezone


class DrugRegistration(forms.ModelForm):
    class Meta:
        model = Drugs
        fields = ['name', 'des', 'category', 'price', 'discount_price', 'batch_no', 'image', 'expiry_date']

    # def __init__(self, request, *args, **kwargs):
    #     # question_pk = kwargs.pop('question_pk')
    #     user_pharmacy = request.user.pharmacyuser.works_at.name
    #     super(DrugRegistration, self).__init__(*args, **kwargs)
    #     if request:
    #         self.fields['pharmacy'].initial = user_pharmacy
    #         self.fields['pharmacy'].widget = forms.HiddenInput()

    def clean_expiry_date(self):
        drug_name = self.cleaned_data['name']
        expiry_date = self.cleaned_data['expiry_date']
        present_date = timezone.now().date()
        difference = int(str(expiry_date - present_date).split()[0])  # gets the number of days difference
        if difference < 1:
            raise forms.ValidationError("{} is expired".format(drug_name))
        elif difference < 7:
            raise forms.ValidationError("{} expiration date is too close".format(drug_name))
        else:
            return expiry_date
