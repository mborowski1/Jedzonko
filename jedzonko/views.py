import random
from .models import Plan, Recipe, DayName, RecipePlan, Page
from django.shortcuts import render, redirect, Http404
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views import View
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):

    def get(self, request):
        recipes = list(Recipe.objects.all().values('name', 'dish_description'))
        random.shuffle(recipes)
        message = 'Dodaj przepis'
        if len(recipes) >= 3:
            return render(request, "index.html", {'recipe1': recipes[0], 'recipe2': recipes[1], 'recipe3': recipes[2]})
        elif len(recipes) == 2:
            return render(request, "index.html", {'recipe1': recipes[0], 'recipe2': recipes[1], 'message': message})
        elif len(recipes) == 1:
            return render(request, "index.html", {'recipe1': recipes[0], 'message': message})
        else:
            return render(request, "index.html", {'message': message})


class DashboardView(View):

    def get(self, request):
        number_of_recipes = Recipe.objects.all().count()
        number_of_plans = Plan.objects.all().count()
        plans_sorted = Plan.objects.all().order_by('-created')
        newest_plan = plans_sorted[0]
        recipe_plans_for_newest_plan = newest_plan.recipeplan_set.all()
        result_dict = {}
        for recipePlan in recipe_plans_for_newest_plan:
            if recipePlan.day_name.name in result_dict.keys():
                result_dict[recipePlan.day_name.name].append(recipePlan)
            else:
                result_dict[recipePlan.day_name.name] = []
                result_dict[recipePlan.day_name.name].append(recipePlan)
            result_dict[recipePlan.day_name.name].sort(key=lambda x: x.order)
        return render(request, "dashboard.html", {'number_of_recipes': number_of_recipes,
                                                  'number_of_plans': number_of_plans,
                                                  'day_recipes': result_dict,
                                                  'newest_plan': newest_plan})


class AddRecipe(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        dish_desc = request.POST.get('dish_description')

        try:
            preparation_time = int(request.POST.get('time'))
        except ValueError:
            messages.info(request, 'Proszę uzupełnić wszystkie pola!')
            return render(request, 'app-add-recipe.html')

        if not name or not ingredients or not description or not preparation_time or not dish_desc:
            messages.info(request, 'Proszę uzupełnić wszystkie pola!')
            return render(request, 'app-add-recipe.html')
        else:
            Recipe.objects.create(name=name, ingredients=ingredients,
                                  description=description, preparation_time=preparation_time, dish_description=dish_desc)
            messages.info(request, 'Przepis został dodany do bazy!')

            return redirect('/recipe/list')


class RecipeDetails(View):
    def get(self, request, id_number):
        recipe = Recipe.objects.get(id=id_number)
        ingredients = list(recipe.ingredients.split(','))
        return render(request, 'app-recipe-details.html', {'recipe': recipe, 'ingredients': ingredients})

    def post(self, request, id_number):
        recipe = Recipe.objects.get(id=id_number)
        if request.POST.get('yes'):
            recipe.votes += 1
            recipe.save()
        elif request.POST.get('no'):
            recipe.votes -= 1
            recipe.save()
        ingredients = list(recipe.ingredients.split(','))
        return render(request, 'app-recipe-details.html', {'recipe': recipe, 'ingredients': ingredients})


class RecipeList(View):

    def get(self, request):
        recipees = Recipe.objects.all().order_by('votes', '-created')
        paginator = Paginator(recipees, 5)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {'recipes': recipes, 'page_range': paginator.page_range})


class RecipeModify(View):

    def get(self, request, id_number):
        try:
            recipe = Recipe.objects.get(id=id_number)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, 'app-edit-recipe.html', {'recipe': recipe})

    def post(self, request, id_number):
        recipe = Recipe.objects.get(id=id_number)
        name = request.POST.get('name')
        desc = request.POST.get('dish_desc')
        time = request.POST.get('time')
        method = request.POST.get('description')
        ingredients = request.POST.get('ingredients')

        if not name or not desc or not time or not method or not ingredients:
            messages.info(request, 'Wszystkie pola muszą być wypełnione!')
            return render(request, 'app-edit-recipe.html', {'recipe': recipe})
        else:
            recipe.name = name
            recipe.dish_description = desc
            recipe.preparation_time = time
            recipe.description = method
            recipe.ingredients = ingredients
            recipe.save()
            messages.info(request, 'Przepis został zmodyfikowany!')
            return redirect('/recipe/list')


class PlanList(View):
    def get(self, request):
        plans_to_pag = Plan.objects.all().only('name', 'description').order_by('name')
        paginator = Paginator(plans_to_pag, 5)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, 'app-schedules.html', {'plans': plans, 'page_range': paginator.page_range})


class PlanDetails(View):

    def get(self, request, id_number):
        plan = Plan.objects.get(pk=id_number)
        recipe_plans = plan.recipeplan_set.all()
        result_dict = {}
        for recipePlan in recipe_plans:
            if recipePlan.day_name.name in result_dict.keys():
                result_dict[recipePlan.day_name.name].append(recipePlan)
            else:
                result_dict[recipePlan.day_name.name] = []
                result_dict[recipePlan.day_name.name].append(recipePlan)
            result_dict[recipePlan.day_name.name].sort(key=lambda x: x.order)
        return render(request, 'app-details-schedules.html', {'plan': plan, 'recipes_by_day': result_dict})


class AddRecipePlan(View):

    def get(self, request):
        ctx = {"plans": Plan.objects.all(),
               "recipes": Recipe.objects.all(),
               "day_names": DayName.objects.all()
               }
        return render(request, "app-schedules-meal-recipe.html", ctx)


    def post(self, request):
        plan = request.POST.get('plan')
        meal_name = request.POST.get('meal_name')
        meal_number = request.POST.get('meal_number')
        recipe = request.POST.get('recipe')
        day_name = request.POST.get('day_name')

        if len(plan) < 1 or len(meal_name) < 1 or len(meal_number) < 1 or len(recipe) < 1 or len(day_name) < 1:
            message = 'Uzupełnij prawidłowo wszystkie pola.'

            ctx = {"plans": Plan.objects.all(),
                   "recipes": Recipe.objects.all(),
                   "day_names": DayName.objects.all(),
                   "message": message
                   }

            return render(request, "app-schedules-meal-recipe.html", ctx)
        RecipePlan.objects.create(meal_name=meal_name, recipe=Recipe.objects.get(id=recipe),
                                  plan=Plan.objects.get(id=plan), order=meal_number,
                                  day_name=DayName.objects.get(id=day_name))
        message = "Dodałeś przepis do planu."
        ctx = {"plans": Plan.objects.all(),
               "recipes": Recipe.objects.all(),
               "day_names": DayName.objects.all(),
               "message": message
               }

        return render(request, "app-schedules-meal-recipe.html", ctx)


class AddPlan(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        plan_name = request.POST.get('plan_name')
        plan_description = request.POST.get('plan_description')

        if len(plan_name) < 1 or len(plan_description) < 1:
            message = 'Uzupełnij prawidłowo wszystkie pola.'

            ctx = {
                "message": message
            }
            return render(request, "app-add-schedules.html", ctx)
        plan = Plan.objects.create(name=plan_name, description=plan_description)
        return redirect(f"/plan/{plan.pk}/")

    
class Contact(View):

    def get(self, request):
        contacts = Page.objects.filter(slug='contact')
        if contacts:
            return render(request, 'contact_template.html', {'contacts': contacts})
        else:
            return redirect('/#contact')


class About(View):

    def get(self, request):
        about = Page.objects.filter(slug='about').first()
        if about:
            return render(request, 'about_application.html', {'about': about})
        else:
            return redirect('/#about')
