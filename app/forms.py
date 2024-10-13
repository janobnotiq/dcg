from django import forms
from .models import Declaration, Company


class DeclarationForm(forms.ModelForm):
    class Meta:
        model = Declaration
        fields = [
            "number_gtd",
            "reference_gtd",
            "date_recorded",
            "customs_mode",
            "sender",
            "reciever",
            "country",
            "custom_price",
            "factor_price",
            "quantity",
            "status",
        ]

        widgets = {
            'date_recorded': forms.DateInput(attrs={
                'type': 'date',  # HTML5 type date, kalendardan tanlash uchun
            }),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name","phone"]