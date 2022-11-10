from recipe.models import Recipe, Ingredient, Instruction, DietType, CuisineType
from rest_framework import serializers
from pprint import pprint


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        #depth = 1 # gets related fields. I guess depth 2 and on would return deeper nested items
        fields = ['id', 'active', 'title', 'diet', 'cuisine_type' ]        

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient

        fields = ['id', 'ingredient', 'ingredient_group' ]

class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ['id', 'step_num', 'instruction' ]

    def create(self, validated_data):
        recipe_id = self.context['recipe_id']       
        return Instruction.objects.create(recipe_id=recipe_id, **validated_data)

class DietTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietType
        fields = ['id', 'diet_type']

class CuisineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuisineType
        fields = ['id', 'cuisine_type']