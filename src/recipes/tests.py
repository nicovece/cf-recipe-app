from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):
    def test_recipe_str_method(self):
        """Test that the string representation returns the recipe name"""
        recipe = Recipe(name="Test Recipe", ingredients="Ingredient1, Ingredient2", cooking_time=10)
        self.assertEqual(str(recipe), "Test Recipe")

    def test_recipe_ingredients_as_list(self):
        """Test converting ingredients string to list"""
        recipe = Recipe(name="Test Recipe", ingredients="Ingredient1, Ingredient2", cooking_time=10)
        self.assertEqual(recipe.return_ingredients_as_list(), ["Ingredient1", "Ingredient2"])

    def test_ingredients_as_list_with_spaces(self):
        """Test ingredients list conversion handles extra spaces properly"""
        recipe = Recipe(name="Test Recipe", ingredients="  Ingredient1 , Ingredient2  ", cooking_time=10)
        self.assertEqual(recipe.return_ingredients_as_list(), ["Ingredient1", "Ingredient2"])

    def test_ingredients_as_list_empty_string(self):
        """Test ingredients list conversion with empty string"""
        recipe = Recipe(name="Test Recipe", ingredients="", cooking_time=10)
        self.assertEqual(recipe.return_ingredients_as_list(), [])

    def test_ingredients_as_list_none_value(self):
        """Test ingredients list conversion with None value"""
        recipe = Recipe(name="Test Recipe", ingredients=None, cooking_time=10)
        self.assertEqual(recipe.return_ingredients_as_list(), [])

    def test_ingredients_as_list_single_ingredient(self):
        """Test ingredients list conversion with single ingredient"""
        recipe = Recipe(name="Test Recipe", ingredients="Single Ingredient", cooking_time=10)
        self.assertEqual(recipe.return_ingredients_as_list(), ["Single Ingredient"])

    def test_calculate_difficulty_easy(self):
        """Test difficulty calculation for easy recipes (short time, few ingredients)"""
        recipe = Recipe(name="Easy Recipe", ingredients="Ingredient1, Ingredient2, Ingredient3", cooking_time=5)
        self.assertEqual(recipe.calculate_difficulty(), "Easy")

    def test_calculate_difficulty_medium(self):
        """Test difficulty calculation for medium recipes (short time, many ingredients)"""
        recipe = Recipe(name="Medium Recipe", ingredients="Ingredient1, Ingredient2, Ingredient3, Ingredient4, Ingredient5", cooking_time=8)
        self.assertEqual(recipe.calculate_difficulty(), "Medium")

    def test_calculate_difficulty_intermediate(self):
        """Test difficulty calculation for intermediate recipes (long time, few ingredients)"""
        recipe = Recipe(name="Intermediate Recipe", ingredients="Ingredient1, Ingredient2", cooking_time=15)
        self.assertEqual(recipe.calculate_difficulty(), "Intermediate")

    def test_calculate_difficulty_hard(self):
        """Test difficulty calculation for hard recipes (long time, many ingredients)"""
        recipe = Recipe(name="Hard Recipe", ingredients="Ingredient1, Ingredient2, Ingredient3, Ingredient4, Ingredient5", cooking_time=20)
        self.assertEqual(recipe.calculate_difficulty(), "Hard")

    def test_calculate_difficulty_boundary_values(self):
        """Test difficulty calculation at boundary values"""
        # Easy boundary: cooking_time < 10 and num_ingredients < 4
        recipe1 = Recipe(name="Easy Boundary", ingredients="Ingredient1, Ingredient2, Ingredient3", cooking_time=9)
        self.assertEqual(recipe1.calculate_difficulty(), "Easy")
        
        # Medium boundary: cooking_time < 10 and num_ingredients >= 4
        recipe2 = Recipe(name="Medium Boundary", ingredients="Ingredient1, Ingredient2, Ingredient3, Ingredient4", cooking_time=9)
        self.assertEqual(recipe2.calculate_difficulty(), "Medium")
        
        # Intermediate boundary: cooking_time >= 10 and num_ingredients < 4
        recipe3 = Recipe(name="Intermediate Boundary", ingredients="Ingredient1, Ingredient2, Ingredient3", cooking_time=10)
        self.assertEqual(recipe3.calculate_difficulty(), "Intermediate")
        
        # Hard boundary: cooking_time >= 10 and num_ingredients >= 4
        recipe4 = Recipe(name="Hard Boundary", ingredients="Ingredient1, Ingredient2, Ingredient3, Ingredient4", cooking_time=10)
        self.assertEqual(recipe4.calculate_difficulty(), "Hard")

    def test_auto_calculate_difficulty_on_save(self):
        """Test that difficulty is automatically calculated when saving"""
        recipe = Recipe(name="Auto Difficulty Recipe", ingredients="Ingredient1, Ingredient2, Ingredient3, Ingredient4", cooking_time=25)
        recipe.save()
        
        # Refresh from database to ensure the save method was called
        recipe.refresh_from_db()
        self.assertEqual(recipe.difficulty, "Hard")

    def test_recipe_creation_with_all_fields(self):
        """Test creating a recipe with all fields populated"""
        recipe = Recipe(
            name="Complete Recipe",
            ingredients="Salt, Pepper, Oil, Garlic",
            cooking_time=30,
            likes=5,
            comments="This is a great recipe!",
            references="https://example.com/recipe"
        )
        recipe.save()
        
        self.assertEqual(recipe.name, "Complete Recipe")
        self.assertEqual(recipe.ingredients, "Salt, Pepper, Oil, Garlic")
        self.assertEqual(recipe.cooking_time, 30)
        self.assertEqual(recipe.likes, 5)
        self.assertEqual(recipe.comments, "This is a great recipe!")
        self.assertEqual(recipe.references, "https://example.com/recipe")
        self.assertEqual(recipe.difficulty, "Hard")  # Should be auto-calculated

    def test_recipe_creation_with_minimal_fields(self):
        """Test creating a recipe with only required fields"""
        recipe = Recipe(
            name="Minimal Recipe",
            ingredients="Ingredient1",
            cooking_time=5
        )
        recipe.save()
        
        self.assertEqual(recipe.name, "Minimal Recipe")
        self.assertEqual(recipe.ingredients, "Ingredient1")
        self.assertEqual(recipe.cooking_time, 5)
        self.assertEqual(recipe.likes, 0)  # Default value
        self.assertEqual(recipe.difficulty, "Easy")  # Auto-calculated

    def test_recipe_field_constraints(self):
        """Test that field constraints are properly enforced"""
        # Test name max length
        long_name = "A" * 121  # Exceeds max_length=120
        recipe = Recipe(name=long_name, ingredients="Test", cooking_time=10)
        
        # This should raise a validation error when saving
        with self.assertRaises(Exception):
            recipe.save()

    def test_recipe_model_meta(self):
        """Test that the model has proper meta configuration"""
        recipe = Recipe(name="Meta Test", ingredients="Test", cooking_time=10)
        self.assertEqual(recipe.recipe_id, None)  # AutoField, not set until saved
        self.assertTrue(hasattr(recipe, 'recipe_id'))  # Should have the field