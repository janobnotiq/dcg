from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from root.models import BaseModel
from datetime import timedelta

User = get_user_model()

# Create your models here.
class Company(BaseModel):
    name = models.CharField(max_length=256,unique=True)
    phone = models.CharField(max_length=50,null=True, blank=True)
    INN = models.CharField(max_length=256)


    def __str__(self) -> str:
        return self.name
    
    # har bir kompaniyaning oylik deklaratsiyalari sonini hisoblash
    def declaration_count(self,month=None):
        if month is None:
            month = timezone.now().month
        
        # Tanlangan oydagi deklaratsiyalarni sanash (updated_at bo'yicha filtrlash)
        return Declaration.objects.filter(
            reciever=self,               # `self` - bu kompaniya
            status=Declaration.Status.FINISHED,
            date_recorded__month=month,      # `date_recorded` bo'yicha oy filtr
            date_recorded__year=timezone.now().year,
        ).count()
    
    def contract_count(self,month=None):
        if month is None:
            month = timezone.now().month
        
        # Tanlangan oydagi deklaratsiyalarni sanash (date_recorded bo'yicha filtrlash)
        return Contract.objects.filter(
            reciever=self,               # `self` - bu kompaniya
            date_recorded__month=month,      # `date_recorded` bo'yicha oy filtr
            date_recorded__year=timezone.now().year,
        ).count()
    
    def dosmotr_count(self,month=None):
        if month is None:
            month = timezone.now().month
        
        # Tanlangan oydagi deklaratsiyalarni sanash (leaving date bo'yicha filtrlash)
        return Dosmotr.objects.filter(
            reciever=self,               # `self` - bu kompaniya
            leaving_date__month=month,      # `leaving_date` bo'yicha oy filtr
            leaving_date__year=timezone.now().year,
        ).count()

    class Meta:
        db_table = 'app_company'
        verbose_name_plural = "Kompaniyalar"


class Declaration(BaseModel):
    
    class Status(models.TextChoices):
        FINISHED = "BOSILDI", "BOSILDI"
        IN_PROCESS = "BOSILMADI", "BOSILMADI"

    
    class Modes(models.TextChoices):
        IM70 = "IM70", "IM 70"
        IM40 = "IM40", "IM 40"
        ND40 = "ND40", "ND 40"
        IM74 = "IM74", "IM 74"
        EK10 = "EK10", "EK 10"
        OTHER = "VABOSHQALAR", "VA BOSHQALAR"

    customs_mode = models.CharField(max_length=20,choices=Modes.choices, verbose_name="Rejimi")
    declarant = models.ForeignKey(User,on_delete=models.CASCADE)
    number_gtd = models.CharField(max_length=256,verbose_name="Nomer gtd")
    reference_gtd = models.CharField(max_length=256)
    date_recorded = models.DateField(verbose_name="Qayd etilgan sana")
    sender = models.CharField(max_length=256)
    reciever = models.ForeignKey(Company,on_delete=models.CASCADE)
    country = models.CharField(max_length=256)
    custom_price = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    factor_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=15,choices=Status.choices)

    @property
    def days_left(self):
        
        today = timezone.now().date()
        expected_day = self.date_recorded + timedelta(days=60)
        return (expected_day - today).days
          
           

    def __str__(self) -> str:
        return f"{self.declarant.first_name} {self.declarant.last_name}ning deklaratsiyasi"
    
    class Meta:
        db_table = 'app_declaration'
        ordering = ["-updated_at",]
        verbose_name_plural = "Deklaratsiyalar"



# Har bir xodimning tanlangan oydagi deklaratsiyalar sonini hisoblaydigan metod
def declaration_count(self, month=None):
    # Hozirgi oyni olish (agar hech narsa berilmagan bo'lsa)
    if month is None:
        month = timezone.now().month
    
    # Tanlangan oydagi deklaratsiyalarni sanash (updated_at bo'yicha filtrlash)
    return Declaration.objects.filter(
        declarant=self,               # `self` - bu xodim (user)
        status=Declaration.Status.FINISHED,
        date_recorded__month=month,      # `date_recorded` bo'yicha oy filtr
        date_recorded__year=timezone.now().year,
    ).count()

# Methodni User modeliga qo'shamiz
User.add_to_class("declaration_count", declaration_count)

class Contract(BaseModel):
    declarant = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.CharField(max_length=256,verbose_name="Tovar")
    transport_service = models.CharField(max_length=256, verbose_name="Transport usluga")
    contract_no = models.CharField(max_length=256, verbose_name="Kontrakt raqami")
    date_recorded = models.DateField(verbose_name="Qayd etilgan sana")
    seller = models.CharField(max_length=256, verbose_name="sotuvchi")
    carrier = models.CharField(max_length=256, verbose_name="tashuvchi")
    reciever = models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name="qabul qiluvchi")

    def __str__(self) -> str:
        return f"{self.declarant.first_name} {self.declarant.last_name}ning kontrakti"
    

    class Meta:
        db_table = 'app_contract'
        ordering = ["-updated_at",]
        verbose_name_plural = "Kontraktlar"


class Dosmotr(BaseModel):
    declarant = models.ForeignKey(User,on_delete=models.CASCADE)
    transport_number = models.CharField(max_length=256,verbose_name="avtotransport raqami")
    product = models.CharField(max_length=256)
    weight = models.CharField(max_length=256, verbose_name="og'irligi")
    arrived_date = models.DateField(verbose_name="yuk kelgan sana")
    leaving_date = models.DateField(verbose_name="yuk ombordan chiqib ketgan sana")
    reciever = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.declarant.first_name} {self.declarant.last_name}ning dosmotri"
    
    class Meta:
        db_table = 'app_dosmotr'
        ordering = ["-updated_at",]
        verbose_name_plural = "Dosmotrlar"
