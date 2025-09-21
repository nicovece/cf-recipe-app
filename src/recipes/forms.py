from django import forms

# Chart type choices - same as in your bookstore project
CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart')
)

# Difficulty choices based on your Recipe model
DIFFICULTY_CHOICES = (
    ('', 'All Difficulties'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard')
)

class RecipeSearchForm(forms.Form):
    # Search criteria fields
    recipe_name = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter recipe name (partial matching supported)'})
    )
    
    ingredients = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter ingredients (comma separated)'})
    )
    
    cooking_time_max = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=1440,
        widget=forms.NumberInput(attrs={'placeholder': 'Max cooking time (minutes)'})
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False
    )
    
    # Chart type selection - same as bookstore
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        required=True,
        initial='#1'
    )
