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
from .models import CuisineType, Recipe, DietType, Instruction, Ingredient, IngredientGroup
from .serializers import RecipeSerializer, DietTypeSerializer, CuisineTypeSerializer, InstructionSerializer, IngredientSerializer

import pprint

# print('###########################')
# print(ingredient_group)
# print('###########################')


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
            if isinstance(request.data['cuisine_type'], int):
                # if enterd data is an int try to get dta from data base
                cuisine_type = CuisineType.objects.get(id=request.data['cuisine_type'])
            # if data is a string check is alphanumeric then attempt to create new ingredient group with suppliet text
            elif isinstance(request.data['cuisine_type'], str): #request.data['ingredient_group'].replace(" ", "").isalnum():
                # create 
                CuisineType.objects.get_or_create(cuisine_type=request.data['cuisine_type'])
                cuisine_type = CuisineType.objects.get(cuisine_type=request.data['cuisine_type'])

            else:
                return Response({'error': 'The cuisine_type entered was not a valid group name or id.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except ObjectDoesNotExist:
            return Response({'error': 'The cuisine_type did not exsits and could not be created.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Replace str from user with id of cuisine type  
        request.data['cuisine_type'] = cuisine_type.pk

        # Standard Create method from here 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

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

        # over ride of create method to modify data posted to cuisine type and diet type    
    def create(self, request, *args, **kwargs):
        # Get POST from browser take str input from user and attemp to get from DB     
        try:
            if isinstance(request.data['ingredient_group'], int):
                # if enterd data is an int try to get dta from data base
                ingredient_group = IngredientGroup.objects.get(id=request.data['ingredient_group'])
            # if data is a string check is alphanumeric then attempt to create new ingredient group with suppliet text
            elif isinstance(request.data['ingredient_group'], str): #request.data['ingredient_group'].replace(" ", "").isalnum():
                # create 
                IngredientGroup.objects.get_or_create(ingredient_group=request.data['ingredient_group'])
                ingredient_group = IngredientGroup.objects.get(ingredient_group=request.data['ingredient_group'])

            else:
                return Response({'error': 'The ingredient group entered was not a valid group name or id.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except ObjectDoesNotExist:
            return Response({'error': 'The ingredient group did not exsits and could not be created.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Replace str from user with id of cuisine type  
        request.data['ingredient_group'] = ingredient_group.pk
        # Standard Create method from here 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)