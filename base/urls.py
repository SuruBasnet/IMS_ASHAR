from django.urls import path
from .views import *


urlpatterns = [
    path('company_info/',CompanyInfoApiView.as_view(),name='company info'),
    path('company_info/<int:pk>/',CompanyInfoIdApiView.as_view(),name='company info detail'),
    path('login/',login,name='login')
]