from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core.exceptions import ValidationError
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
import os
from .models import Recipe
from .admin import RecipeAdmin
from .views import HomeView, RecipeListView, RecipeDetailView

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

    def test_short_description_field(self):
        """Test short_description field functionality"""
        # Test creating recipe with short_description
        recipe = Recipe(
            name="Test Recipe",
            ingredients="Ingredient1, Ingredient2",
            cooking_time=30,
            short_description="A delicious test recipe"
        )
        recipe.save()
        
        self.assertEqual(recipe.short_description, "A delicious test recipe")
        
        # Test creating recipe without short_description (should be blank)
        recipe2 = Recipe(
            name="Test Recipe 2",
            ingredients="Ingredient1",
            cooking_time=15
        )
        recipe2.save()
        
        self.assertEqual(recipe2.short_description, "")

    def test_short_description_max_length(self):
        """Test short_description field max length constraint"""
        # Test with description at max length (300 characters)
        max_desc = "A" * 300
        recipe = Recipe(
            name="Test Recipe",
            ingredients="Ingredient1",
            cooking_time=30,
            short_description=max_desc
        )
        try:
            recipe.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for max length description")
        
        # Note: TextField with max_length doesn't enforce validation at model level
        # The max_length is mainly for form validation and database hints
        # So we just test that it can be saved
        recipe.save()
        self.assertEqual(len(recipe.short_description), 300)

    def test_recipe_image_field_default(self):
        """Test recipe_image field default value"""
        recipe = Recipe(
            name="Test Recipe",
            ingredients="Ingredient1",
            cooking_time=30
        )
        recipe.save()
        
        # Should have default image
        self.assertEqual(recipe.recipe_image.name, "no_picture.png")

    def test_recipe_image_field_upload(self):
        """Test recipe_image field with uploaded image"""
        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name, 'JPEG')
        temp_file.close()
        
        try:
            with open(temp_file.name, 'rb') as f:
                uploaded_file = SimpleUploadedFile(
                    "test_image.jpg",
                    f.read(),
                    content_type="image/jpeg"
                )
            
            recipe = Recipe(
                name="Test Recipe",
                ingredients="Ingredient1",
                cooking_time=30,
                recipe_image=uploaded_file
            )
            recipe.save()
            
            # Check that image was saved
            self.assertTrue(recipe.recipe_image.name.startswith('recipes/'))
            self.assertTrue(recipe.recipe_image.name.endswith('.jpg'))
            
        finally:
            # Clean up
            os.unlink(temp_file.name)
            if recipe.recipe_image and os.path.exists(recipe.recipe_image.path):
                os.unlink(recipe.recipe_image.path)


class RecipeViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test recipes
        self.recipe1 = Recipe.objects.create(
            name="Test Recipe 1",
            ingredients="Ingredient1, Ingredient2",
            cooking_time=30,
            short_description="A test recipe"
        )
        
        self.recipe2 = Recipe.objects.create(
            name="Test Recipe 2",
            ingredients="Ingredient3, Ingredient4, Ingredient5",
            cooking_time=45,
            short_description="Another test recipe"
        )

    def test_home_view(self):
        """Test HomeView renders correctly"""
        response = self.client.get(reverse('recipes:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/home.html')

    def test_recipe_list_view(self):
        """Test RecipeListView renders correctly with recipes"""
        response = self.client.get(reverse('recipes:recipe-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/list.html')
        self.assertIn('recipes', response.context)
        self.assertEqual(len(response.context['recipes']), 2)
        self.assertIn(self.recipe1, response.context['recipes'])
        self.assertIn(self.recipe2, response.context['recipes'])

    def test_recipe_list_view_empty(self):
        """Test RecipeListView with no recipes"""
        # Delete all recipes
        Recipe.objects.all().delete()
        
        response = self.client.get(reverse('recipes:recipe-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/list.html')
        self.assertIn('recipes', response.context)
        self.assertEqual(len(response.context['recipes']), 0)

    def test_recipe_detail_view(self):
        """Test RecipeDetailView renders correctly"""
        response = self.client.get(reverse('recipes:recipe-detail', kwargs={'pk': self.recipe1.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')
        self.assertIn('recipe', response.context)
        self.assertEqual(response.context['recipe'], self.recipe1)

    def test_recipe_detail_view_not_found(self):
        """Test RecipeDetailView with non-existent recipe"""
        response = self.client.get(reverse('recipes:recipe-detail', kwargs={'pk': 999}))
        
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_context(self):
        """Test RecipeDetailView context contains correct data"""
        response = self.client.get(reverse('recipes:recipe-detail', kwargs={'pk': self.recipe1.pk}))
        
        recipe = response.context['recipe']
        self.assertEqual(recipe.name, "Test Recipe 1")
        self.assertEqual(recipe.ingredients, "Ingredient1, Ingredient2")
        self.assertEqual(recipe.cooking_time, 30)
        self.assertEqual(recipe.short_description, "A test recipe")
        self.assertEqual(recipe.difficulty, "Intermediate")  # Auto-calculated

    def test_recipe_list_view_context(self):
        """Test RecipeListView context contains correct data"""
        response = self.client.get(reverse('recipes:recipe-list'))
        
        recipes = response.context['recipes']
        self.assertEqual(len(recipes), 2)
        
        # Check that recipes are ordered correctly (by creation order)
        self.assertEqual(recipes[0], self.recipe1)
        self.assertEqual(recipes[1], self.recipe2)


class RecipeURLTest(TestCase):
    def test_home_url(self):
        """Test home URL pattern"""
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
        
        # Test URL resolution
        resolved = resolve('/')
        self.assertEqual(resolved.func.__name__, HomeView.as_view().__name__)

    def test_recipe_list_url(self):
        """Test recipe list URL pattern"""
        url = reverse('recipes:recipe-list')
        self.assertEqual(url, '/recipes/')
        
        # Test URL resolution
        resolved = resolve('/recipes/')
        self.assertEqual(resolved.func.__name__, RecipeListView.as_view().__name__)

    def test_recipe_detail_url(self):
        """Test recipe detail URL pattern"""
        url = reverse('recipes:recipe-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/recipes/1/')
        
        # Test URL resolution
        resolved = resolve('/recipes/1/')
        self.assertEqual(resolved.func.__name__, RecipeDetailView.as_view().__name__)
        self.assertEqual(int(resolved.kwargs['pk']), 1)

    def test_url_namespace(self):
        """Test that URLs use correct namespace"""
        # Test that URLs are namespaced correctly
        self.assertEqual(reverse('recipes:home'), '/')
        self.assertEqual(reverse('recipes:recipe-list'), '/recipes/')
        self.assertEqual(reverse('recipes:recipe-detail', kwargs={'pk': 1}), '/recipes/1/')


class RecipeTemplateTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.recipe = Recipe.objects.create(
            name="Template Test Recipe",
            ingredients="Ingredient1, Ingredient2, Ingredient3",
            cooking_time=25,
            short_description="A recipe for testing templates",
            references="https://example.com/recipe"
        )

    def test_home_template_content(self):
        """Test home template renders expected content"""
        response = self.client.get(reverse('recipes:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe App')  # Assuming this is in the template

    def test_recipe_list_template_content(self):
        """Test recipe list template renders expected content"""
        response = self.client.get(reverse('recipes:recipe-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to our')
        self.assertContains(response, 'Recipes List!')
        self.assertContains(response, 'Template Test Recipe')
        self.assertContains(response, 'A recipe for testing templates')
        self.assertContains(response, 'View')
        self.assertContains(response, 'Recipe')

    def test_recipe_list_template_no_recipes(self):
        """Test recipe list template with no recipes"""
        Recipe.objects.all().delete()
        
        response = self.client.get(reverse('recipes:recipe-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')

    def test_recipe_detail_template_content(self):
        """Test recipe detail template renders expected content"""
        response = self.client.get(reverse('recipes:recipe-detail', kwargs={'pk': self.recipe.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Template Test Recipe')
        self.assertContains(response, 'A recipe for testing templates')
        self.assertContains(response, 'Ingredients')
        self.assertContains(response, 'Ingredient1')
        self.assertContains(response, 'Ingredient2')
        self.assertContains(response, 'Ingredient3')
        self.assertContains(response, '25 minutes')
        self.assertContains(response, 'Intermediate')  # Auto-calculated difficulty (25 min, 3 ingredients)
        self.assertContains(response, 'View Reference')
        self.assertContains(response, 'https://example.com/recipe')
        self.assertContains(response, 'Like (0)')

    def test_recipe_detail_template_without_reference(self):
        """Test recipe detail template without reference URL"""
        self.recipe.references = ""
        self.recipe.save()
        
        response = self.client.get(reverse('recipes:recipe-detail', kwargs={'pk': self.recipe.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'View Reference')

    def test_recipe_detail_template_without_short_description(self):
        """Test recipe detail template without short description"""
        self.recipe.short_description = ""
        self.recipe.save()
        
        response = self.client.get(reverse('recipes:recipe-detail', kwargs={'pk': self.recipe.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Template Test Recipe')
        # Short description should not be rendered if empty

    def test_base_template_inheritance(self):
        """Test that templates extend base template"""
        response = self.client.get(reverse('recipes:home'))
        
        self.assertEqual(response.status_code, 200)
        # Check that base template is used (assuming it has a title block)
        self.assertContains(response, '<title>')  # Assuming base template has title


class RecipeAdminTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.site = AdminSite()
        self.admin = RecipeAdmin(Recipe, self.site)
        
        # Create test user and recipe
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        
        self.recipe = Recipe.objects.create(
            name="Admin Test Recipe",
            ingredients="Ingredient1, Ingredient2",
            cooking_time=30,
            short_description="A recipe for testing admin"
        )

    def test_admin_registration(self):
        """Test that Recipe model is registered in admin"""
        from django.contrib import admin
        self.assertTrue(admin.site.is_registered(Recipe))

    def test_admin_list_display(self):
        """Test admin list display configuration"""
        expected_fields = ['name', 'cooking_time', 'difficulty', 'likes']
        self.assertEqual(self.admin.list_display, expected_fields)

    def test_admin_list_filter(self):
        """Test admin list filter configuration"""
        expected_filters = ['difficulty', 'cooking_time']
        self.assertEqual(self.admin.list_filter, expected_filters)

    def test_admin_search_fields(self):
        """Test admin search fields configuration"""
        expected_search_fields = ['name', 'ingredients']
        self.assertEqual(self.admin.search_fields, expected_search_fields)

    def test_admin_readonly_fields(self):
        """Test admin readonly fields configuration"""
        expected_readonly_fields = ['difficulty', 'likes', 'comments']
        self.assertEqual(self.admin.readonly_fields, expected_readonly_fields)

    def test_admin_fieldsets(self):
        """Test admin fieldsets configuration"""
        fieldsets = self.admin.fieldsets
        
        # Check that fieldsets exist
        self.assertIsNotNone(fieldsets)
        self.assertEqual(len(fieldsets), 3)
        
        # Check fieldset structure
        basic_info = fieldsets[0]
        self.assertEqual(basic_info[0], 'Basic Information')
        self.assertIn('name', basic_info[1]['fields'])
        self.assertIn('short_description', basic_info[1]['fields'])
        self.assertIn('ingredients', basic_info[1]['fields'])
        self.assertIn('cooking_time', basic_info[1]['fields'])
        self.assertIn('recipe_image', basic_info[1]['fields'])
        
        calculated_fields = fieldsets[1]
        self.assertEqual(calculated_fields[0], 'Calculated Fields')
        self.assertIn('difficulty', calculated_fields[1]['fields'])
        self.assertIn('likes', calculated_fields[1]['fields'])
        self.assertIn('comments', calculated_fields[1]['fields'])
        self.assertIn('collapse', calculated_fields[1]['classes'])
        
        additional_info = fieldsets[2]
        self.assertEqual(additional_info[0], 'Additional Information')
        self.assertIn('references', additional_info[1]['fields'])

    def test_admin_changelist_view(self):
        """Test admin changelist view"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/recipes/recipe/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Test Recipe')
        self.assertContains(response, '30')
        self.assertContains(response, 'Intermediate')  # Auto-calculated difficulty
        self.assertContains(response, '0')  # Default likes

    def test_admin_change_view(self):
        """Test admin change view"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(f'/admin/recipes/recipe/{self.recipe.pk}/change/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Test Recipe')
        self.assertContains(response, 'A recipe for testing admin')
        self.assertContains(response, 'Ingredient1, Ingredient2')
        self.assertContains(response, '30')
        self.assertContains(response, 'Intermediate')  # Readonly field
        self.assertContains(response, '0')  # Readonly field