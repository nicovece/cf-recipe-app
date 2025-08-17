from django.test import TestCase
from django.core.exceptions import ValidationError
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

    def test_ingredients_as_list_with_empty_ingredients(self):
        """Test ingredients list conversion filters out empty ingredients"""
        recipe = Recipe(name="Test Recipe", ingredients="Ingredient1, , Ingredient2,  , Ingredient3", cooking_time=10)
        self.assertEqual(recipe.return_ingredients_as_list(), ["Ingredient1", "Ingredient2", "Ingredient3"])

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
        # Test name max length using full_clean() which will validate the constraint
        long_name = "A" * 121  # Exceeds max_length=120
        recipe = Recipe(name=long_name, ingredients="Test", cooking_time=10)
        
        # This should raise a validation error when validating
        with self.assertRaises(ValidationError):
            recipe.full_clean()
        
        # Test that a name exactly at the limit works
        exact_length_name = "A" * 120  # Exactly max_length=120
        recipe = Recipe(name=exact_length_name, ingredients="Test", cooking_time=10)
        try:
            recipe.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for name at max length")

    def test_cooking_time_validators(self):
        """Test cooking time field validators"""
        # Test minimum value validator
        recipe = Recipe(name="Test Recipe", ingredients="Test", cooking_time=0)
        with self.assertRaises(ValidationError):
            recipe.full_clean()
        
        # Test maximum value validator
        recipe = Recipe(name="Test Recipe", ingredients="Test", cooking_time=1441)
        with self.assertRaises(ValidationError):
            recipe.full_clean()
        
        # Test valid values
        recipe = Recipe(name="Test Recipe", ingredients="Test", cooking_time=1)
        try:
            recipe.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for valid cooking time 1")
        
        recipe = Recipe(name="Test Recipe", ingredients="Test", cooking_time=1440)
        try:
            recipe.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for valid cooking time 1440")

    def test_recipe_model_meta(self):
        """Test that the model has proper meta configuration"""
        recipe = Recipe(name="Meta Test", ingredients="Test", cooking_time=10)
        self.assertEqual(recipe.recipe_id, None)  # AutoField, not set until saved
        self.assertTrue(hasattr(recipe, 'recipe_id'))  # Should have the field

    def test_validation_empty_name(self):
        """Test validation fails with empty name"""
        recipe = Recipe(name="", ingredients="Test ingredient", cooking_time=10)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_validation_whitespace_name(self):
        """Test validation fails with whitespace-only name"""
        recipe = Recipe(name="   ", ingredients="Test ingredient", cooking_time=10)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_validation_empty_ingredients(self):
        """Test validation fails with empty ingredients"""
        recipe = Recipe(name="Test Recipe", ingredients="", cooking_time=10)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_validation_whitespace_ingredients(self):
        """Test validation fails with whitespace-only ingredients"""
        recipe = Recipe(name="Test Recipe", ingredients="   ", cooking_time=10)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_validation_zero_cooking_time(self):
        """Test validation fails with zero cooking time"""
        recipe = Recipe(name="Test Recipe", ingredients="Test ingredient", cooking_time=0)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_validation_negative_cooking_time(self):
        """Test validation fails with negative cooking time"""
        recipe = Recipe(name="Test Recipe", ingredients="Test ingredient", cooking_time=-5)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_validation_cooking_time_too_high(self):
        """Test validation fails with cooking time exceeding 24 hours"""
        recipe = Recipe(name="Test Recipe", ingredients="Test ingredient", cooking_time=1441)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_validation_valid_recipe(self):
        """Test validation passes with valid recipe data"""
        recipe = Recipe(name="Valid Recipe", ingredients="Ingredient1, Ingredient2", cooking_time=30)
        try:
            recipe.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly!")