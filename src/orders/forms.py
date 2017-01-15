from django import forms
from .models import Country, Province, City, County, Order
# from smart_selects.form_fields import ChainedModelChoiceField

class OrderCreateForm(forms.ModelForm):

#    province = ChainedModelChoiceField('orders', 'Province', 'country', 'country', 'orders', 'Country', 'name', False, False)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'country', 'province', 'city', 'county',
                  'address', 'postal_code']