from django import forms
from app.models import Contract,Dosmotr


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            "product",
            "transport_service",
            "date_recorded",
            "contract_no",
            "seller",
            "carrier",
            "reciever",
        ]

        widgets = {
            'date_recorded': forms.DateInput(attrs={
                'type': 'date',  # HTML5 type date, kalendardan tanlash uchun
            }),
        }


class DosmotrForm(forms.ModelForm):
    class Meta:
        model = Dosmotr
        fields = [
            "reciever",
            "transport_number",
            "product",
            "weight",
            "arrived_date",
            "leaving_date",
        ]

        widgets = {
            'arrived_date': forms.DateInput(attrs={
                'type': 'date',  # HTML5 type date, kalendardan tanlash uchun
            }),
            'leaving_date': forms.DateInput(attrs={
                'type': 'date',  # HTML5 type date, kalendardan tanlash uchun
            }),
        }

