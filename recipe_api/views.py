from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeSerializer

# Create Recipe
class RecipeCreateAPIView(APIView):
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Read (Get all Recipes)
class RecipeListAPIView(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        if not recipes:
            return Response({"message": "No recipes found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

# Read (Get a single Recipe)
class RecipeDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

# Update Recipe
class RecipeUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Recipe
class RecipeDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        
        recipe.delete()
        return Response({"message": "Recipe deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
