"""scrumlab URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko.views import IndexView, DashboardView, AddRecipe, AddPlan, AddRecipePlan, \
    RecipeModify, PlanDetails, PlanList, RecipeList, RecipeDetails, Contact, About

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('main/', DashboardView.as_view()),
    path('recipe/add/', AddRecipe.as_view(), name='add_recipe'),
    path('recipe/list/', RecipeList.as_view(), name='list_of_recipes'),
    path('recipe/<int:id_number>/', RecipeDetails.as_view(), name='recipe_details'),
    path('recipe/modify/<int:id_number>/', RecipeModify.as_view(), name='recipe_modify'),
    path('plan/add/', AddPlan.as_view(), name='add_plan'),
    path('plan/add-recipe/', AddRecipePlan.as_view(), name='add_recipe_plan'),
    path('plan/<int:id_number>/', PlanDetails.as_view(), name='plan_details'),
    path('plan/list/', PlanList.as_view(), name='list_of_plans'),
    path('contact/', Contact.as_view(), name='contact'),
    path('about/', About.as_view(), name='about_application'),
]
