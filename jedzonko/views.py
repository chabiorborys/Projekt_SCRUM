from datetime import datetime
from random import shuffle
from typing import List

from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe, Plan
from django.core.paginator import Paginator, EmptyPage, InvalidPage


class IndexView(View):

    # def get(self, request):
    #     ctx = {"actual_date": datetime.now()}
    #     return render(request, "app-recipes.html", ctx)

    def as_view(request):
        return render(request, 'index.html')


def dashboard(request):
    count_plan = Plan.objects.all().count()
    summary = Recipe.objects.all().count

    last_plan = list(Plan.objects.all().order_by('-created'))[0]
    recipes = last_plan.recepieplan_set.all()

    recipes_lst = []

    for i in range(1, 8):
        tmp = recipes.filter(day_name=i)
        if tmp:
            recipes_lst.append(tmp.order_by('order'))

    return render(request, 'dashboard.html',
                  {'count_plan': count_plan, 'last_plan': last_plan, 'summary_recipes': summary, 'recipes_lst': recipes_lst})


def karuzela(request):
    recepises = list(Recipe.objects.all())
    shuffle(recepises)
    recipe1 = recepises[0]
    recipe2 = recepises[1]
    recipe3 = recepises[2]
    return render(request, "index.html", {"recipe1": recipe1, "recipe2": recipe2, "recipe3": recipe3})



def plan_list (request):
    plans_list = Plan.objects.all().order_by("name")
    paginator = Paginator(plans_list, 1)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        plans = paginator.page(page)
    except(EmptyPage, InvalidPage):
        plans = paginator.page(page)

    return render(request, "app-schedules.html", {"plans": plans})

def new_recipe(request):
    if request.method == "GET":
        return render(request, "app-add-recipe.html")
    elif request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        preparation_time = request.POST["preparation_time"]
        ingredients = request.POST["ingredients"]
        preparation_details=request.POST["preparation_details"]
        message = "Wypełnij poprawnie wszystkie pola"
        if len(name) == 0 or len(description) == 0 or len(ingredients) == 0 or int(preparation_time) == 0:
            return render(request, "app-add-recipe.html", {'message': message})
        else:
            Recipe.objects.create(name=name, description=description, preparation_time=preparation_time, preparation_details=preparation_details, ingredients=ingredients, votes=0)
            return redirect('/recipe/list/')

def new_plan(request):
    if request.method == "GET":
        return render(request, "app-add-schedules.html")
    elif request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        message = "Wypełnij poprawnie wszystkie pola"
        if len(name) == 0 or len(description) == 0:
            return render(request, "app-add-schedules.html", {'message': message})
        else:
            Plan.objects.create(name=name, description=description)
            return redirect('/plan/<INT:id>/details')



class App_recpies(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "app-recipes.html", ctx)

def as_view(request):
    recipies_list = Recipe.objects.all().order_by("-votes")
    #return render(request, "app-recipes.html", {"recipies": recipies_list})
    paginator = Paginator(recipies_list, 50)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        recipies = paginator.page(page)
    except(EmptyPage, InvalidPage):
        recipies = paginator.page(page)

    return render(request, "app-recipes.html", {"recipies": recipies})


def landing_page(request):
    return render(request, 'landing_page.html')


def recipe_details(request):
    return render(request, 'app-recipe-details.html')


def app_add_recipe(request):
    return render(request, 'app-add-recipe.html')


def app_edit_recipe(request):
    return render(request, 'app-edit-recipe.html')


def app_details_schedules(request):
    return render(request, 'app-details-schedules.html'),


def add_app_add_schedules(request):
    return render(request, 'app-add-schedules.html')


def app_schedules_meal_recipe(request):
    return render(request, 'app-schedules-meal-recipe.html')


def app_schedules(request):
    return render(request, 'app-schedules.html')




