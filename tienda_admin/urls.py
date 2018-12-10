from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    #path('', views.post_list, name='post_list'),
    #path('', views.login, name='login'),
    path('page_logout/',views.logout, name='page_logout'),
	#path('', TemplateView.as_view(template_name='home.html'), name='home'), #IMPORTANTE home quando nao existe view, só a pagina html :)
	path('', include('django.contrib.auth.urls')), #entra com endereco site/login, qualquer coisa incluir accounts/ no url e no site fica site /accounts/login
	#path('signup/', views.SignUp.as_view(), name='signup'),
    path('', TemplateView.as_view(template_name='welcome.html'), name='welcome'),
    path('home/', views.home, name='home'),
	path('signup/', views.signup, name='signup'),
    path('customer_registration/', views.customer_registration, name='customer_registration'),
    path('product_registration/', views.product_registration, name='product_registration'),
    path('payment_type_registration/', views.payment_registration, name='payment_type_registration'),
	path('report_daily/', views.report_daily, name='report_daily'),
	path('income_outcome_registration/', views.income_outcome_registration, name='income_outcome_registration'),
    path('export/xls/', views.export_xls, name='export_xls'),
	path('report_customer/', views.report_customer, name='report_customer'),
	path('report_income_outcome_registration/', views.report_income_outcome_registration, name='report_income_outcome_registration'),
	path('report_customer_comparation/', views.report_customer_comparation, name='report_customer_comparation'),
	path('report_comparation/', views.report_comparation, name='report_comparation'),


]
