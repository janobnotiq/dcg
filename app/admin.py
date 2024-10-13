from django.contrib import admin
from .models import Company, Declaration
from unfold.admin import ModelAdmin


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    ordering = ["-created_at",]


@admin.register(Declaration)
class DeclarationAdmin(ModelAdmin):
    list_display = ["declarant__first_name","declarant__last_name","status","updated_at"]
    ordering = ["-created_at",]