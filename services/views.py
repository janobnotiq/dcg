from django.shortcuts import render
from app.models import Company
from .forms import ContractForm, DosmotrForm

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def company_report(request,pk):
    selected_month = request.GET.get('month', datetime.now().month)

    company = Company.objects.filter(id=pk).last()

    context = {
        "company": company,
        "declarations": company.declaration_count(month=selected_month),
        "contracts": company.contract_count(month=selected_month),
        "dosmotrs": company.dosmotr_count(month=selected_month),
        "current_month": int(selected_month) if selected_month else datetime.now().month,
    }

    return render(request,"company-report.html",context)


@login_required
def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)  # Hozircha saqlamaymiz
            contract.declarant = request.user   # Deklarantni user bilan bog'laymiz
            contract.save()  # Endi ma'lumotni saqlaymiz
            return redirect('contract-success')  
    else:
        form = ContractForm()
    
    return render(request, 'add-contract.html', {'form': form})

# deklaratsiya muvaffaqiyatli qo'shildi sahifasi uchun
@login_required
def contract_success_view(request):
    return render(request,"contract-success.html")

@login_required
def add_dosmotr(request):
    if request.method == 'POST':
        form = DosmotrForm(request.POST)
        if form.is_valid():
            dosmotr = form.save(commit=False)  # Hozircha saqlamaymiz
            dosmotr.declarant = request.user   # Deklarantni user bilan bog'laymiz
            dosmotr.save()  # Endi ma'lumotni saqlaymiz
            return redirect('dosmotr-success')  
    else:
        form = DosmotrForm()
    
    return render(request, 'add-dosmotr.html', {'form': form})

# deklaratsiya muvaffaqiyatli qo'shildi sahifasi uchun
@login_required
def dosmotr_success_view(request):
    return render(request,"dosmotr-success.html")