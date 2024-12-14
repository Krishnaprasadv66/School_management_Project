from django.urls import path
from .views import  AdminLoginView, LibraryHistoryView,FeesHistoryView, StudentView, UserListView, UserDetailView

urlpatterns = [
    
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('library-history/', LibraryHistoryView.as_view(), name='library_history_list'),
    path('fees-history/', FeesHistoryView.as_view(), name='fees_history_list'),
    path('students/', StudentView.as_view(), name='student_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
]