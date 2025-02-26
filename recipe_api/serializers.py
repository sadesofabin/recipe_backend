from rest_framework import serializers
from django.contrib.auth.models import User
from recipe_api.models import UserDetails, UserProfile, SavedRecipe

class UserRegisterSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField(required=False, allow_blank=True)
    lastname = serializers.CharField(required=False, allow_blank=True)
    phonenumber = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'firstname', 'lastname', 'phonenumber']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        firstname = validated_data.pop('firstname', '')
        lastname = validated_data.pop('lastname', '')
        phonenumber = validated_data.pop('phonenumber', None)

        # Create User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=firstname,  
            last_name=lastname     
        )

        # Create UserDetails (without username)
        UserDetails.objects.create(
            user=user,
            email=user.email,
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):  # Renamed serializer
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()  # Updated related name

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class SavedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRecipe
        fields = ['id','user', 'title','image', 'ingredients', 'instructions', 'created_at', 'updated_at', 'deleted_at']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'  # Or specify fields manually