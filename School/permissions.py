from rest_framework.permissions import BasePermission


# PERMISSIONS

# PERMISSION FOR ADMIN ONLY
class IsAdminUser(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


    




class IsLibrarianReadonlyUser(BasePermission):
   
    def has_permission(self, request, view):
        
        if request.user and request.user.role == 'librarian':
            return request.method in ['GET']
        
        # Allow other users (admins or office staff) to perform any operation
        return True
    



class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        # Allow admins to have full access (CRUD operations)
        if request.user and request.user.role == 'admin':
            return True
        
        # Librarians and office staff can only read (GET requests)
        if request.user and request.user.role in ['librarian', 'office_staff']:
            
            if request.method == 'GET':
                return True

        return False

    def has_object_permission(self, request, view, obj):
        # Admins can do any operation on any object (CRUD operations)
        if request.user and request.user.role == 'admin':
            return True
        
        if request.user and request.user.role in ['librarian', 'office_staff']:
            if request.method == 'GET':
                return True

        return False