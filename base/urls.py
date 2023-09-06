from django.urls import path
from .views import *


urlpatterns = [
    path('company_info/',CompanyInfoApiView.as_view(),name='home')
]