from django.contrib import admin
from .models import Company, Declaration, Contract, Dosmotr
from unfold.admin import ModelAdmin


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    ordering = ["-created_at",]


@admin.register(Declaration)
class DeclarationAdmin(ModelAdmin):
    list_display = ["declarant__first_name","declarant__last_name","status","updated_at"]
    ordering = ["-created_at",]
    

@admin.register(Contract)
class ContractAdmin(ModelAdmin):
    list_display = ["product","transport_service","reciever","declarant__first_name","declarant__last_name","date_recorded"]
    ordering = ["-date_recorded",]
    

@admin.register(Dosmotr)
class DosmotrAdmin(ModelAdmin):
    list_display = ["product","weight","declarant__first_name","declarant__last_name","arrived_date","leaving_date"]
    ordering = ["-leaving_date",]