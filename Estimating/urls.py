from django.urls import path
from . import views
from .views import save_doors

urlpatterns = [
    path('', views.estimating_list_view, name='estimating-list'),
    path('run-email-parser/', views.run_email_parser, name='run_email_parser'),
    path('estimating/fetch/', views.fetch_emails_view, name='fetch_emails'),
    path('api/save-doors/', save_doors, name='save_doors'),

]
