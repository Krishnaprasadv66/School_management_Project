from django.urls import path
from .views import OfficeStaffLoginView

urlpatterns = [
    
    path('login/', OfficeStaffLoginView.as_view(), name='office-staff-login'),
    
    
]