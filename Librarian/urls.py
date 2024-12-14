from django.urls import path
from .views import  LibrarianLoginView

urlpatterns = [
    
    path('login/', LibrarianLoginView.as_view(), name='librarian-login'),
    
]