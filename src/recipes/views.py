from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Recipe
from .forms import RecipeSearchForm
from .utils import get_all_charts
import pandas as pd
import re

def process_wildcard_search(search_term):
    """
    Process wildcard search terms and convert them to Django Q objects
    
    Supports:
    - * wildcards: "pasta*" matches "pasta", "pastas", "pasta-based"
    - ? wildcards: "pasta?" matches "pasta" but not "pastas"
    - Partial matching: "pasta" matches "Pasta al Pesto"
    """
    if not search_term:
        return None
    
    # Remove extra whitespace
    search_term = search_term.strip()
    
    # Handle wildcards
    if '*' in search_term or '?' in search_term:
        # Convert wildcards to regex patterns
        # * becomes .* (any characters)
        # ? becomes . (single character)
        pattern = search_term.replace('*', '.*').replace('?', '.')
        
        # Create Q object for regex matching
        return Q(name__iregex=pattern)
    else:
        # Regular partial matching (case-insensitive)
        return Q(name__icontains=search_term)

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
    charts = None

    if request.method == "POST":
        # Get form data
        search_action = request.POST.get("search_action")
        recipe_name = request.POST.get("recipe_name")
        ingredients = request.POST.get("ingredients")
        cooking_time_max = request.POST.get("cooking_time_max")
        difficulty = request.POST.get("difficulty")

        # Start with all recipes
        qs = Recipe.objects.all()

        # Apply filters only if user clicked "Search & Analyze" (not "Analyze All Recipes")
        if search_action == "search":
            # Apply filters based on form data (AND logic)
            if recipe_name:
                # Use wildcard processing for recipe names
                name_query = process_wildcard_search(recipe_name)
                if name_query:
                    qs = qs.filter(name_query)
            
            if ingredients:
                # Split ingredients by comma and search for each one with wildcard support
                ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",") if ingredient.strip()]
                for ingredient in ingredient_list:
                    if '*' in ingredient or '?' in ingredient:
                        # Handle wildcards in ingredients
                        pattern = ingredient.replace('*', '.*').replace('?', '.')
                        qs = qs.filter(ingredients__iregex=pattern)
                    else:
                        # Regular partial matching for ingredients
                        qs = qs.filter(ingredients__icontains=ingredient)
            
            if cooking_time_max:
                qs = qs.filter(cooking_time__lte=int(cooking_time_max))
            
            if difficulty:
                qs = qs.filter(difficulty=difficulty)
        
        # If search_action == "show_all", no filters are applied (qs remains Recipe.objects.all())

        # Convert QuerySet to DataFrame if we have results
        if qs.exists():
            recipes_df = pd.DataFrame(qs.values())
            
            # Add calculated columns
            recipes_df["ingredient_count"] = recipes_df["ingredients"].apply(
                lambda x: len([ing.strip() for ing in x.split(",") if ing.strip()]) if x else 0
            )
            
            # Make recipe names clickable links to detail pages
            recipes_df["name"] = recipes_df.apply(
                lambda row: f'<a href="/recipes/{row["id"]}/" class="font-semibold text-accent-600 hover:text-accent-800 hover:underline">{row["name"]}</a>',
                axis=1
            )
            
            # Generate all charts
            charts = get_all_charts(recipes_df, labels=recipes_df["name"].values)
            
            # Convert DataFrame to HTML for display with custom CSS class
            recipes_df = recipes_df.to_html(escape=False, classes='search-results-table', table_id='search-results')

    context = {"form": form, "recipes_df": recipes_df, "charts": charts}
    return render(request, "recipes/search.html", context)