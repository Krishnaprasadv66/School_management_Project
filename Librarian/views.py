from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from School.models import LibraryHistory, FeesHistory, Student
from .serializers import  UserLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from School.permissions import IsAdminUser

# Create your views here.




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
    

