from django.urls import path
from .views import company_report, contract_success_view, \
    add_contract, dosmotr_success_view, add_dosmotr \
    ,ContractUpdateView,DosmotrUpdateView


urlpatterns = [
    path("company-report/<int:pk>/", company_report, name="company-report"),

    # kontrakt
    path("add-contract/", add_contract, name="add-contract"),
    path("update-contract/<int:pk>/", ContractUpdateView.as_view(), name="update-contract"),
    path("contract-success/", contract_success_view, name="contract-success"),

    #dosmotr
    path("dosmotr-success/", dosmotr_success_view, name="dosmotr-success"),
    path("update-dosmotr/<int:pk>/", DosmotrUpdateView.as_view(), name="update-dosmotr"),
    path("add-dosmotr/", add_dosmotr, name="add-dosmotr"),
]