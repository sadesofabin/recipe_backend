from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recipe_api.models import UserDetails, UserProfile
from recipe_api.serializers import UserRegisterSerializer, UserSerializer, UserDetailsSerializer, UserProfileSerializer
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


# class UserProfileView(APIView):
#     def get(self, request, user_id):
#         try:
#             # Using select_related to fetch the profile with the user in one query
#             user = User.objects.select_related('profile').get(id=user_id)
#             serializer = UserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class UserProfileView(APIView):
    def get(self, request, user_id):
        try:
            # Fetch UserDetails and UserProfile using select_related for optimization
            user = User.objects.get(id=user_id)
            user_details = UserDetails.objects.select_related('user').get(user=user)

            # Serialize both models
            details_serializer = UserDetailsSerializer(user_details)

            # Combine data from both serializers
            combined_data = {
                'user': user.username,
                'email': user_details.email,
                'firstname': user_details.firstname,
                'lastname': user_details.lastname,
                'phonenumber': user_details.phonenumber,
                'created_at': user_details.created_at,
                'updated_at': user_details.updated_at
            }

            return Response(combined_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except UserDetails.DoesNotExist:
            return Response({'error': 'User details not found'}, status=status.HTTP_404_NOT_FOUND)
