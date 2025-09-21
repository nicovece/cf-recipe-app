from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import RecipeSearchForm
from .utils import get_chart
import pandas as pd

class HomeView(TemplateView):
    template_name = 'recipes/home.html'


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'


@login_required
def recipe_search(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None  # Initialize recipes_df
    chart = None

    if request.method == "POST":
        # Get form data
        recipe_name = request.POST.get("recipe_name")
        ingredients = request.POST.get("ingredients")
        cooking_time_max = request.POST.get("cooking_time_max")
        difficulty = request.POST.get("difficulty")
        chart_type = request.POST.get("chart_type")

        # Start with all recipes
        qs = Recipe.objects.all()

        # Apply filters based on form data (AND logic)
        if recipe_name:
            qs = qs.filter(name__icontains=recipe_name)
        
        if ingredients:
            # Split ingredients by comma and search for each one
            ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",") if ingredient.strip()]
            for ingredient in ingredient_list:
                qs = qs.filter(ingredients__icontains=ingredient)
        
        if cooking_time_max:
            qs = qs.filter(cooking_time__lte=int(cooking_time_max))
        
        if difficulty:
            qs = qs.filter(difficulty=difficulty)

        # Convert QuerySet to DataFrame if we have results
        if qs.exists():
            recipes_df = pd.DataFrame(qs.values())
            
            # Add calculated columns
            recipes_df["ingredient_count"] = recipes_df["ingredients"].apply(
                lambda x: len([ing.strip() for ing in x.split(",") if ing.strip()]) if x else 0
            )
            
            # Generate chart
            chart = get_chart(chart_type, recipes_df, labels=recipes_df["name"].values)
            
            # Convert DataFrame to HTML for display
            recipes_df = recipes_df.to_html()

    context = {"form": form, "recipes_df": recipes_df, "chart": chart}
    return render(request, "recipes/search.html", context)