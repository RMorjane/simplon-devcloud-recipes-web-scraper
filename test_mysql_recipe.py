import unittest
from mysql_recipe_scraper import MySQLRecipe

class TestMySQLRecipe(unittest.TestCase):

    def test_connect(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        connection = mysql_recipe.connection
        self.assertTrue(connection)

    def test_add_ingredient(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        ingredient_id = mysql_recipe.add_ingredient("poivron rouge")   
        self.assertFalse(ingredient_id==0)

    def test_get_ingredient_id(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        ingredient_id = mysql_recipe.get_ingredient_id("poivron rouge")
        self.assertFalse(ingredient_id==0)

    def test_add_ingredient_usage(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        usage_id = mysql_recipe.add_ingredient_usage("Pour l'assaisonnement")  
        self.assertFalse(usage_id==0)

    def test_get_usage_id(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        usage_id = mysql_recipe.get_usage_id("Pour l'assaisonnement")  
        self.assertFalse(usage_id==0)

    def test_add_recipe(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        recipe_id = mysql_recipe.add_recipe("Recette pancake à la confiture maison",
        "https://www.atelierdeschefs.fr/fr/recette/11881-pancake-a-la-confiture-maison.php",
        "https://www.atelierdeschefs.com/media/recette-d11881-pancake-a-la-confiture-maison.jpg") 
        self.assertFalse(recipe_id==0)

    def test_get_recipe_id(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        recipe_id = mysql_recipe.get_recipe_id("Recette pancake à la confiture maison")
        self.assertFalse(recipe_id==0)

    def test_add_recipe_ingredient(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        recipe_ingredient_id = mysql_recipe.add_recipe_ingredient(11,31,10,6,2,'g') 
        self.assertFalse(recipe_ingredient_id==None)

    def test_add_step_recipe(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        step_recipe_id = mysql_recipe.add_step_recipe(11,"1. POUR LA PATE",
        "Mélanger 1 kg de farine avec 1 Litre d'eau")
        self.assertFalse(step_recipe_id==None)

    def test_find_recipes(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.connect()
        mysql_recipe.find_recipes({
            "recipe_name": "crêpe"
        })
        list_recipes = mysql_recipe.list_recipes
        self.assertFalse(len(list_recipes)==0)

if __name__ == '__main__':
    unittest.main()