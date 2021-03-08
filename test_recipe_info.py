import unittest
from mysql_recipe_scraper import RecipeInfo

class TestRecipeInfo(unittest.TestCase):

    def test_read_infos(self):
        href = "/fr/recette/16580-crepes-faciles-au-chocolat.php"
        recipe_info = RecipeInfo(href)
        recipe_info.read_infos()
        data_ok = (
            recipe_info.recipe_name=="" 
            and recipe_info.persons_count==0 
            and len(recipe_info.list_usages)==0 
            and len(recipe_info.list_ingredients)==0 
            and len(recipe_info.list_steps)==0
        )
        self.assertTrue(data_ok)        

if __name__ == '__main__':
    unittest.main()