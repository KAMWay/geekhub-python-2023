from django import forms


class OrderForm(forms.Form):
    product_id = forms.IntegerField(min_value=0)
    product_quantity = forms.IntegerField(min_value=1)
