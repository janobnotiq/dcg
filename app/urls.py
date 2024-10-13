from django.urls import path
from .views import home_view
from django.contrib.auth import views as auth_views
from .views import logout_view, add_declaration, declaration_success_view\
    , add_company, declaration_list_view, in_process_declarations\
    , employees_list, companies_list, DeclarationUpdateView, DeclarationReportView \
    , DeclarationFilterView


urlpatterns = [
    path("",home_view,name="home"),
    path("accounts/login/",auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/",logout_view, name="logout"),
    path("add-declaration/",add_declaration, name="add-declaration"),
    path("declaration-success/", declaration_success_view, name="declaration-success"),
    path("add-company/",add_company, name="add-company"),
    path("my-declarations/",declaration_list_view, name="my-declarations"),
    path("in-process-declarations/",in_process_declarations, name="in-process"),
    path("update-declaration/<int:pk>/",DeclarationUpdateView.as_view(), name="update-declaration"),
    
    # for director
    path("employees/",employees_list, name="employees"),
    path("companies/", companies_list, name="companies"),
    path("declarant-report/<int:declarant_id>/", DeclarationReportView.as_view(), name="declarant-report"),
    path("declarant-report/<str:username>/", DeclarationFilterView.as_view(), name="filter-report"),
]
