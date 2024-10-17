from django.urls import path
from .views import home_view
from django.contrib.auth import views as auth_views
from .views import logout_view, add_declaration, declaration_success_view\
    , add_company, declaration_list_view, in_process_declarations\
    , employees_list, companies_list, my_services_view, my_contracts_view,my_dosmotrs_view \
    ,delete_contract,delete_declaration,delete_dosmotr\
    , DeclarationFilterView, DeclarationUpdateView, DeclarationReportView


urlpatterns = [
    path("",home_view,name="home"),
    path("accounts/login/",auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/",logout_view, name="logout"),
    path("add-declaration/",add_declaration, name="add-declaration"),
    path("declaration-success/", declaration_success_view, name="declaration-success"),
    path("add-company/",add_company, name="add-company"),
    path("my-declarations/",declaration_list_view, name="my_declarations"),
    path("my-contracts/",my_contracts_view, name="my_contracts"),
    path("my-dosmotrs/",my_dosmotrs_view, name="my_dosmotrs"),
    path("my-services/",my_services_view, name="my-services"),
    path("in-process-declarations/",in_process_declarations, name="in-process"),
    path("update-declaration/<int:pk>/",DeclarationUpdateView.as_view(), name="update-declaration"),
    path("delete-declaration/<int:pk>/",delete_declaration, name="delete-declaration"),
    path("delete-dosmotr/<int:pk>/",delete_dosmotr, name="delete-dosmotr"),
    path("delete-contract/<int:pk>/",delete_contract, name="delete-contract"),
    
    # for director
    path("employees/",employees_list, name="employees"),
    path("companies/", companies_list, name="companies"),
    path("declarant-report/<int:declarant_id>/", DeclarationReportView.as_view(), name="declarant-report"),
    path("declarant-report/<str:username>/", DeclarationFilterView.as_view(), name="filter-report"),
]
