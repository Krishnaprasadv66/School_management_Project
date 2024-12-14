from django.urls import path
from .views import UserRegistrationView, AdminLoginView, OfficeStaffLoginView, LibrarianLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/admin/', AdminLoginView.as_view(), name='admin-login'),
    path('login/office-staff/', OfficeStaffLoginView.as_view(), name='office-staff-login'),
    path('login/librarian/', LibrarianLoginView.as_view(), name='librarian-login'),
    
]