
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class DietType(models.Model):
    diet_type = models.CharField(max_length=255)

class CuisineType(models.Model):
    cuisine_type = models.CharField(max_length=255)

class Recipe(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    diet = models.ForeignKey(DietType, on_delete=models.PROTECT)
    cuisine_type = models.ForeignKey(CuisineType, on_delete=models.PROTECT)

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    step_num = models.SmallIntegerField()
    instruction = models.TextField()

class IngredientGroup(models.Model):
    ingredient_group = models.CharField(max_length=255)

class Ingredient(models.Model):
    ingredient = models.CharField(max_length=255)
    ingredient_group = models.ForeignKey(IngredientGroup, default=1, on_delete=models.PROTECT)

class RecipeIngredient(models.Model):

    class Units(models.TextChoices):
        TEASPOON = 'TSP', _('Teaspoon')
        TABLESPOON = 'TBL', _('Tablespoon')
        CUP = 'CUP', _('Cup')
        MILLILITER = 'MIL', _('Milliliter')
        LITER = 'LIT', _('Liter')
        GRAM = 'GRM', _('Gram')
        KILOGRAM = 'KLG', _('Kilogram')
        WHOLE = 'WHL', _('Whole')

    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT, related_name='recipes')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, related_name='ingredients')
    quantity = models.DecimalField(max_digits=4, decimal_places=2)
    unit = models.CharField(max_length=3, choices=Units.choices, default=Units.WHOLE)
