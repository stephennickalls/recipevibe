from django.shortcuts import render

# from store.pagination import DefaultPagination
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
# from .filters import ProductFilter
from .models import CuisineType, Recipe, DietType, Instruction, Ingredient
from .serializers import RecipeSerializer, DietTypeSerializer, CuisineTypeSerializer, InstructionSerializer, IngredientSerializer

import pprint

def has_numbers(input):
        return any(char.isdigit() for char in input)

class RecipeViewSet(ModelViewSet):
    # queryset = Recipe.objects.select_related('diet').all()
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    

    def get_serializer_context(self):
        return {'request': self.request}

    # over ride of create method to modify data posted to cuisine type and diet type    
    def create(self, request, *args, **kwargs):

        # Get POST from browser take str input from user and attemp to get from DB
        try:
            if not has_numbers(request.data['cuisine_type']):
                cuisine_type = CuisineType.objects.get(cuisine_type=request.data['cuisine_type'])
            else:
                return Response({'error': 'Recipe cannot be created because there were numbers in the cuisine type attribute.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except ObjectDoesNotExist:
            CuisineType.objects.create(cuisine_type=request.data['cuisine_type'])
            cuisine_type = CuisineType.objects.get(cuisine_type=request.data['cuisine_type'])

        # Replace str from user with id of cuisine type  
        request.data['cuisine_type'] = cuisine_type.pk

        # Standard Create method from here 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class DietTypeViewSet(ModelViewSet):
    queryset = DietType.objects.all()
    serializer_class = DietTypeSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CuisineTypeViewSet(ModelViewSet):
    queryset = CuisineType.objects.all()
    serializer_class = CuisineTypeSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class InstructionViewSet(ModelViewSet):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer

    # filters Instruction to show only those for the current recipe
    def get_queryset(self):
        return Instruction.objects.filter(recipe_id=self.kwargs['recipe_pk']).order_by('step_num')


    def get_serializer_context(self):
        return {'recipe_id': self.kwargs['recipe_pk']}



class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_serializer_context(self):
        return {'request': self.request}