# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LibraryHistory, FeesHistory, Student
from .serializers import UserRegistrationSerializer, UserLoginSerializer, FeesHistorySerializer, LibraryHistorySerializer, StudentSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUser




# registration for (Admin, Office Staff, Librarian)

class UserRegistrationView(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Save the user and return the success response
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully.",
                    "user": {
                        "email": user.email,
                        "full_name": user.full_name,
                        "role": user.get_role_display(),
                    }
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


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



# OFFICE STAFF LOGIN
class OfficeStaffLoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to attempt login
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Check if the user is office staff
            if user.role != 'office_staff':
                return Response({"error": "Not authorized for office staff login."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Try to create the refresh and access tokens
            try:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response({
                    'message': 'Welcome Office Staff...!',
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




# LIBRARIAN LOGIN
class LibrarianLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Check if the user is a librarian
            if user.role != 'librarian':
                return Response(
                    {"error": "Not authorized for librarian login."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'message': 'Welcome Librarian...!',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.get_role_display(),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



