import unittest
from mysql_recipe_scraper import RecipeCategory

class TestRecipeCategory(unittest.TestCase):

    def test_read_infos(self):
        url_recipes = "https://www.atelierdeschefs.fr/fr/recettes-de-crepes-au-chocolat.php"
        recipe_category = RecipeCategory(url_recipes)
        recipe_category.read_infos()
        my_links = recipe_category.links
        self.assertFalse(len(my_links)==0)

    def test_save_mysql_recipe(self):
        url_recipes = "https://www.atelierdeschefs.fr/fr/recettes-de-crepes-au-chocolat.php"
        recipe_category = RecipeCategory(url_recipes)
        recipe_category.read_infos()
        my_links = recipe_category.links
        self.assertTrue("href" in my_links[0])          

if __name__ == '__main__':
    unittest.main()