from django.views.generic import TemplateView, ListView, DetailView
from .models import Recipe

class HomeView(TemplateView):
    template_name = 'recipes/home.html'


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'