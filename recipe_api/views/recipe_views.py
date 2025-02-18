from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recipe_api.models import UserDetails
from recipe_api.serializers import UserRegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class UpdateUserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def put(self, request):
        user = request.user  # Get logged-in user

        try:
            user_details = UserDetails.objects.get(user=user)
        except UserDetails.DoesNotExist:
            return Response({"message": "User details not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update `UserDetails` Model
        serializer = UserRegisterSerializer(user_details, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Update `User` Model separately (no duplicate checking)
            user.username = request.data.get('username', user.username)
            user.email = request.data.get('email', user.email)
            user.first_name = request.data.get('firstname', user.first_name)
            user.last_name = request.data.get('lastname', user.last_name)
            user.save()

            return Response({"message": "User details updated successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request, user_id):
        try:
            # Using select_related to fetch the profile with the user in one query
            user = User.objects.select_related('profile').get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
