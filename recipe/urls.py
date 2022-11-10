from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('diettypes', views.DietTypeViewSet, basename='diettypes')
router.register('cuisinetypes', views.CuisineTypeViewSet, basename='cuisinetypes')

recipes_router = routers.NestedDefaultRouter(router, 'recipes', lookup='recipe')
recipes_router.register('instructions', views.InstructionViewSet, basename='recipe-instructions')
recipes_router.register('ingredients', views.IngredientViewSet, basename='recipe-ingredients')


urlpatterns = router.urls + recipes_router.urls