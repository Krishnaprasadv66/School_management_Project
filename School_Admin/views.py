# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from School.models import LibraryHistory, FeesHistory, Student, User
from School.serializers import  UserLoginSerializer 
from .serializers import FeesHistorySerializer, LibraryHistorySerializer, StudentSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from School.permissions import IsAdminUser, IsLibrarianReadonlyUser





        


# LOGIN FUNCTIONS

# ADMIN LOGIN
class AdminLoginView(APIView):
    permission_classes = [AllowAny]  
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Check if the user is an admin
            if user.role != 'admin':
                return Response({"error": "Not authorized for admin login."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Try to create the refresh and access tokens
            try:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response({
                    'message': 'Welcome Admin...!',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'email': user.email,
                        'full_name': user.full_name,
                        'role': user.get_role_display(),
                    }
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Error generating tokens: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    
# library history view


class LibraryHistoryView(APIView):
    permission_classes = [IsLibrarianReadonlyUser]  

    def get(self, request, *args, **kwargs):
        
        library_history = LibraryHistory.objects.all()
        serializer = LibraryHistorySerializer(library_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Create a new LibraryHistory record
        serializer = LibraryHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, id):
        try:
            return LibraryHistory.objects.get(id=id)
        except LibraryHistory.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        # Expecting 'id' in the request body
        id = request.data.get('id')
        if not id:
            return Response({"error": "'id' is required to update the details."}, status=status.HTTP_400_BAD_REQUEST)

        library_history = self.get_object(id)
        if library_history is None:
            return Response({"error": "LibraryHistory not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LibraryHistorySerializer(library_history, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Expecting 'id' and a confirmation flag in the request body
        id = request.data.get('id')
        confirm = request.data.get('confirm', False)

        if not id:
            return Response({"error": "'id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        if not confirm:
            return Response({"error": "Please provide confirmation to delete this record."}, status=status.HTTP_400_BAD_REQUEST)

        library_history = self.get_object(id)
        if library_history is None:
            return Response({"error": "LibraryHistory not found."}, status=status.HTTP_404_NOT_FOUND)

        # Perform the delete operation if confirmed
        library_history.delete()
        return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)





# FeesHistory View (CRUD operations)

class FeesHistoryView(APIView):
    permission_classes = [IsLibrarianReadonlyUser]  

    def get(self, request, *args, **kwargs):
        
        fees_history = FeesHistory.objects.all()
        serializer = FeesHistorySerializer(fees_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Create a new FeesHistory record
        serializer = FeesHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, id):
        try:
            return FeesHistory.objects.get(id=id)
        except FeesHistory.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        # Expecting 'id' in the request body
        id = request.data.get('id')
        if not id:
            return Response({"error": "'id' is required to update the details."}, status=status.HTTP_400_BAD_REQUEST)

        fees_history = self.get_object(id)
        if fees_history is None:
            return Response({"error": "FeesHistory not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeesHistorySerializer(fees_history, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Expecting 'id' and a confirmation flag in the request body
        id = request.data.get('id')
        confirm = request.data.get('confirm', False)

        if not id:
            return Response({"error": "'id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        if not confirm:
            return Response({"error": "Please provide confirmation to delete this record."}, status=status.HTTP_400_BAD_REQUEST)

        fees_history = self.get_object(id)
        if fees_history is None:
            return Response({"error": "FeesHistory not found."}, status=status.HTTP_404_NOT_FOUND)

        # Perform the delete operation if confirmed
        fees_history.delete()
        return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

# admin and office staff can manage students details but librarian can only view this
class StudentView(APIView):
    permission_classes = [IsLibrarianReadonlyUser]  

    def get(self, request, *args, **kwargs):
        """ Get all students """
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ Create a new student """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, id):
        try:
            return Student.objects.get(id=id)
        except Student.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        """ Update a student """
        id = request.data.get('id')
        if not id:
            return Response({"error": "'id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        student = self.get_object(id)
        if student is None:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)  # Use partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """ Delete a student with confirmation """
        id = request.data.get('id')
        confirm = request.data.get('confirm', False)  # Check for confirmation

        if not id:
            return Response({"error": "'id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        student = self.get_object(id)
        if student is None:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        # If the confirmation is not provided or is False, do not proceed with the deletion
        if not confirm:
            return Response({"error": "Please confirm the deletion by passing 'confirm': true in the request."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the deletion after confirmation
        student.delete()
        return Response({"message": f"Student {student.first_name} {student.last_name} deleted successfully."}, 
                        status=status.HTTP_204_NO_CONTENT)
    



# CRUD OPERATION FOR OFFICE STAFF AND LIBRARIAN

class UserListView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        """ List all users (office staff and librarian), with optional full_name search """
        full_name = request.query_params.get('full_name', None)  # Get full_name query param (optional)

        if full_name:
            users = User.objects.filter(role__in=['office_staff', 'librarian'], full_name__icontains=full_name)
        else:
            users = User.objects.filter(role__in=['office_staff', 'librarian'])

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Create a new user (office staff or librarian) """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # This will create the user
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can access

    def get_object(self, data):
        """ Helper method to get a user by ID (passed in the body) """
        try:
            user_id = data.get('id')  # Expecting 'id' in the request body
            return User.objects.get(id=user_id, role__in=['office_staff', 'librarian'])
        except User.DoesNotExist:
            return None

    def get(self, request):
        """ Get details of a specific user (using ID passed in the body) """
        user = self.get_object(request.data)
        if user is None:
            return Response({"error": "User not found or invalid role"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """ Update a specific user (office staff or librarian), with ID in the body """
        user = self.get_object(request.data)
        if user is None:
            return Response({"error": "User not found or invalid role"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """ Delete a specific user (office staff or librarian), with confirmation and ID in the body """
        user = self.get_object(request.data)
        if user is None:
            return Response({"error": "User not found or invalid role"}, status=status.HTTP_404_NOT_FOUND)

        confirm = request.data.get('confirm', False)  # Expecting confirmation flag in the body

        if not confirm:
            return Response({"error": "Please confirm deletion by setting 'confirm' to true in the request body."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({"message": f"User {user.full_name} has been deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)