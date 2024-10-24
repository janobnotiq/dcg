from datetime import datetime
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.views import View
from django.db.models import Q

from .forms import DeclarationForm, CompanyForm
from .models import Declaration, Company, Contract, Dosmotr

# bosh sahifa uchun view
@login_required
def home_view(request):
    user = request.user
    cont = {
        "user":user,
    }
    return render(request,"index.html",context=cont)

# tizimdan chiqish
def logout_view(request):
    logout(request)
    return redirect("login")

# dekalaratsiya qo'shish
@login_required
def add_declaration(request):
    if request.method == 'POST':
        form = DeclarationForm(request.POST)
        if form.is_valid():
            declaration = form.save(commit=False)  # Hozircha saqlamaymiz
            declaration.declarant = request.user   # Deklarantni user bilan bog'laymiz
            declaration.save()  # Endi ma'lumotni saqlaymiz
            return redirect('declaration-success')  # Muvaffaqiyatli deklaratsiya uchun yo'naltirish
    else:
        form = DeclarationForm()
    
    return render(request, 'add-declaration.html', {'form': form})

# deklaratsiya muvaffaqiyatli qo'shildi sahifasi uchun
@login_required
def declaration_success_view(request):
    return render(request,"declaration-success.html")

# kompaniya qo'shish
@login_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            return redirect('home')  # Muvaffaqiyatli deklaratsiya uchun yo'naltirish
    else:
        form = CompanyForm()
    
    return render(request, 'add-company.html', {'form': form})

# xodimning bugungi qilgan deklaratsiyalari
@login_required
def my_services_view(request):
    return render(request,"my-services.html")

@login_required
def declaration_list_view(request):
    mode = request.GET.get('mode')
    print(mode)
    if mode is None or mode == "all":
        declarations = Declaration.objects.filter(
            declarant=request.user,
            )
    else:
        declarations = Declaration.objects.filter(
            declarant=request.user,
            customs_mode=mode
        )

    count = declarations.filter(
        date_recorded__month=timezone.now().month,
        date_recorded__year=timezone.now().year).count()

    if declarations.count() > 20:
        declarations = declarations[:20]
    
    return render(
        request,
        "my_declarations.html",
        {
            "declarations":declarations,
            "mode":mode,
            "count":count
            }
        )

# jarayondagi deklaratsiyalar
@login_required
def in_process_declarations(request):
    declarations = Declaration.objects.filter(
        Q(declarant=request.user) & 
        (
            Q(customs_mode=Declaration.Modes.ND40) | Q(customs_mode=Declaration.Modes.IM70)
            )
        )
    return render(request,"in-process-declarations.html",{"declarations":declarations})

# xodimlar ro'yhati
@login_required
def employees_list(request):
    if request.user.is_superuser:
        selected_month = request.GET.get('month', timezone.now().month)
        employees = User.objects.filter(is_staff=False)
        for employee in employees:
            employee.declaration_count = employee.declaration_count(month=selected_month)

        return render(request,"employees.html",{
            "employees":employees,
            "current_month": int(selected_month) if selected_month else timezone.now().month,
            })
    else:
        employees = User.objects.filter(id=request.user.pk)
        return render(request,"employees.html",{"employees":employees})

# kompaniyalar ro'yhati
@login_required
def companies_list(request):
    companies = Company.objects.all()
    selected_month = request.GET.get('month', timezone.now().month)

    for company in companies:
            company.declaration_count = company.declaration_count(month=selected_month)

    return render(
        request,
        "companies.html",
        {
            "companies":companies,
            "current_month": int(selected_month) if selected_month else datetime.now().month,
            }
            )

# deklaratsiyaning statusini yangilash
class DeclarationUpdateView(LoginRequiredMixin,UpdateView):
    model = Declaration
    form_class = DeclarationForm
    template_name = "update-declaration.html"
    success_url = reverse_lazy("my_declarations")

    def get_queryset(self):
        return Declaration.objects.filter(declarant=self.request.user)
    


class DeclarationReportView(View):
    def get(self, request, declarant_id):
        # Foydalanuvchi ID'si bilan deklaratsiyalarni olish
        declarant = User.objects.filter(id=declarant_id).last()
        declarations = Declaration.objects.filter(declarant=declarant,status=Declaration.Status.FINISHED)

        return render(request, 'declarant-report.html', {
            'declarations': declarations,
            'count': declarations.count(),
            'declarant': declarant,
        })

class DeclarationFilterView(View):
    def post(self, request, username):
        declarant = User.objects.filter(username=username).last()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Foydalanuvchi ID'si bilan sanalar oralig'idagi deklaratsiyalarni olish
        declarations = Declaration.objects.filter(
            declarant=declarant,
            date_recorded__gte=start_date,
            date_recorded__lte=end_date,
            status=Declaration.Status.FINISHED,
        )

        return render(request, 'declarant-report-filter.html', {
            'declarations': declarations,
            'count': declarations.count(),
            'declarant': declarant,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
        })


@login_required
def my_contracts_view(request):
    contracts = Contract.objects.filter(declarant=request.user).all()
    count = Contract.objects.filter(declarant=request.user,date_recorded__month=timezone.now().month).count()
    return render(request,"my-contracts.html",{"contracts":contracts,"count":count})

@login_required
def my_dosmotrs_view(request):
    dosmotrs = Dosmotr.objects.filter(declarant=request.user).all()
    count = Dosmotr.objects.filter(declarant=request.user,leaving_date__month=timezone.now().month).count()
    return render(request,"my-dosmotrs.html",{"dosmotrs":dosmotrs,"count":count})

@login_required
def delete_declaration(request,pk):
    declaration = get_object_or_404(Declaration,id=pk,declarant=request.user)
    if declaration is not None:
        declaration.delete()
    return redirect('my_declarations')

@login_required
def delete_dosmotr(request,pk):
    dosmotr = get_object_or_404(Dosmotr,id=pk,declarant=request.user)
    if dosmotr is not None:
        dosmotr.delete()
    return redirect('my_dosmotrs')

@login_required
def delete_contract(request,pk):
    contract = get_object_or_404(Contract,id=pk,declarant=request.user)
    if contract is not None:
        contract.delete()
    return redirect('my_contracts')

class ContractReportView(View):
    def get(self, request, declarant_id):
        # Foydalanuvchi ID'si bilan deklaratsiyalarni olish
        declarant = User.objects.filter(id=declarant_id).last()
        contracts = Contract.objects.filter(declarant=declarant).all()

        return render(request, 'contract-report.html', {
            'contracts': contracts,
            'count': contracts.count(),
            'declarant': declarant,
        })
    

class ContractFilterView(View):
    def post(self, request, declarant_id):
        declarant = User.objects.filter(id=declarant_id).last()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Foydalanuvchi ID'si bilan sanalar oralig'idagi deklaratsiyalarni olish
        contracts = Contract.objects.filter(
            declarant=declarant,
            date_recorded__gte=start_date,
            date_recorded__lte=end_date,
        )

        return render(request, 'contract-filter.html', {
            'contracts': contracts,
            'count': contracts.count(),
            'declarant': declarant,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
        })
    

class DosmotrReportView(View):
    def get(self, request, declarant_id):
        # Foydalanuvchi ID'si bilan deklaratsiyalarni olish
        declarant = User.objects.filter(id=declarant_id).last()
        dosmotrs = Dosmotr.objects.filter(declarant=declarant).all()

        return render(request, 'dosmotr-report.html', {
            'dosmotrs': dosmotrs,
            'count': dosmotrs.count(),
            'declarant': declarant,
        })
    

class DosmotrFilterView(View):
    def post(self, request, declarant_id):
        declarant = User.objects.filter(id=declarant_id).last()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Foydalanuvchi ID'si bilan sanalar oralig'idagi deklaratsiyalarni olish
        dosmotrs = Dosmotr.objects.filter(
            declarant=declarant,
            leaving_date__gte=start_date,
            leaving_date__lte=end_date,
        )

        return render(request, 'dosmotr-filter.html', {
            'dosmotrs': dosmotrs,
            'count': dosmotrs.count(),
            'declarant': declarant,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
        })
    

def employee_report(request,username):
    employee = get_object_or_404(User,username=username)
    selected_month = request.GET.get('month',timezone.now().month)
    declaration_count = Declaration.objects.filter(declarant=employee,date_recorded__month=selected_month).count()
    contract_count = Contract.objects.filter(declarant=employee,date_recorded__month=selected_month).count()
    dosmotr_count = Dosmotr.objects.filter(declarant=employee,leaving_date__month=selected_month).count()
    print(selected_month)
    return render(
        request,
        "employee-report.html",
        {
            "declaration_count":declaration_count,
            "contract_count":contract_count,
            "dosmotr_count":dosmotr_count,
            "employee":employee,
            "current_month":int(selected_month)
        }
    )


class CompanyDeclarationReportView(View):
    def get(self, request, pk):
        # Foydalanuvchi ID'si bilan deklaratsiyalarni olish
        company = Company.objects.filter(id=pk).last()
        declarations = Declaration.objects.filter(reciever=company)

        return render(request, 'company-declaration-report.html', {
            'declarations': declarations,
            'count': declarations.count(),
            'company': company,
        })


class CompanyDeclarationFilterView(View):
    def post(self, request, pk):
        company = Company.objects.filter(id=pk).last()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Foydalanuvchi ID'si bilan sanalar oralig'idagi deklaratsiyalarni olish
        declarations = Declaration.objects.filter(
            reciever=company,
            date_recorded__gte=start_date,
            date_recorded__lte=end_date,
        )

        return render(request, 'company-declaration-filter.html', {
            'declarations': declarations,
            'count': declarations.count(),
            'company': company,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
        })
    

class CompanyContractReportView(View):
    def get(self, request, pk):
        # Foydalanuvchi ID'si bilan deklaratsiyalarni olish
        company = Company.objects.filter(id=pk).last()
        contracts = Contract.objects.filter(reciever=company).all()

        return render(request, 'company-contract-report.html', {
            'contracts': contracts,
            'count': contracts.count(),
            'company': company,
        })
    

class CompanyContractFilterView(View):
    def post(self, request, pk):
        company = Company.objects.filter(id=pk).last()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Foydalanuvchi ID'si bilan sanalar oralig'idagi deklaratsiyalarni olish
        contracts = Contract.objects.filter(
            reciever=company,
            date_recorded__gte=start_date,
            date_recorded__lte=end_date,
        )

        return render(request, 'company-contract-filter.html', {
            'contracts': contracts,
            'count': contracts.count(),
            'company': company,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
        })
    

class CompanyDosmotrReportView(View):
    def get(self, request, pk):
        # Foydalanuvchi ID'si bilan deklaratsiyalarni olish
        company = Company.objects.filter(id=pk).last()
        dosmotrs = Dosmotr.objects.filter(reciever=company).all()

        return render(request, 'company-dosmotr-report.html', {
            'dosmotrs': dosmotrs,
            'count': dosmotrs.count(),
            'company': company,
        })
    

class CompanyDosmotrFilterView(View):
    def post(self, request, pk):
        company = Company.objects.filter(id=pk).last()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
            start_date = timezone.make_aware(start_date, timezone.get_current_timezone())

        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
            end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

        # Foydalanuvchi ID'si bilan sanalar oralig'idagi deklaratsiyalarni olish
        dosmotrs = Dosmotr.objects.filter(
            reciever=company,
            leaving_date__gte=start_date,
            leaving_date__lte=end_date,
        )

        return render(request, 'company-dosmotr-filter.html', {
            'dosmotrs': dosmotrs,
            'count': dosmotrs.count(),
            'company': company,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
        })