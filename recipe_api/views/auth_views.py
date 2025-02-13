from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from recipe_api.serializers import UserRegisterSerializer
from django.contrib.auth.models import User
from recipe_api.models import UserDetails
from django.db.utils import IntegrityError


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)
        
        return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create User (Serializer already handles UserDetails)
                serializer.save()

                return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

            except IntegrityError:
                return Response({"error": "A user with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Debugging: Print serializer errors
        print("Serializer Errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
