from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recipe_api.models import SavedRecipe
from recipe_api.serializers import SavedRecipeSerializer
from rest_framework.permissions import IsAuthenticated

class SavedRecipeView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures that the user must be authenticated

    # POST: Create a new saved recipe
    def post(self, request):
        title = request.data.get('title')
        ingredients = request.data.get('ingredients')
        instructions = request.data.get('instructions')

        if not title or not ingredients or not instructions:
            return Response({"error": "All fields (title, ingredients, instructions) are required."}, status=status.HTTP_400_BAD_REQUEST)

        saved_recipe = SavedRecipe.objects.create(
            user=request.user,  # Use the authenticated user
            title=title,
            ingredients=ingredients,
            instructions=instructions
        )

        return Response(SavedRecipeSerializer(saved_recipe).data, status=status.HTTP_201_CREATED)

    # GET: Retrieve saved recipes for the authenticated user, excluding deleted ones
    def get(self, request):
        # Filter the saved recipes for the authenticated user and exclude deleted recipes
        saved_recipes = SavedRecipe.objects.filter(user=request.user, deleted_at__isnull=True)

        # Serialize the list of saved recipes, including 'id'
        return Response(SavedRecipeSerializer(saved_recipes, many=True).data)

    # DELETE: Soft delete a saved recipe (set deleted_at timestamp)
    def delete(self, request, pk):
        try:
            saved_recipe = SavedRecipe.objects.get(pk=pk, user=request.user)
            
            # Set the deleted_at field to current time
            saved_recipe.deleted_at = timezone.now()
            saved_recipe.save()

            return Response({"message": "Saved recipe deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except SavedRecipe.DoesNotExist:
            return Response({'error': 'Saved recipe not found or not owned by this user.'}, status=status.HTTP_404_NOT_FOUND)
