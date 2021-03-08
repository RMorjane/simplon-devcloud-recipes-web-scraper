from mysql_recipe_scraper import RecipeCategory

if __name__ == '__main__':

    url_recipes = "https://www.atelierdeschefs.fr/fr/recettes-de-crepes-au-chocolat.php"
    recipe_category = RecipeCategory(url_recipes)
    recipe_category.read_infos()
    recipe_category.display()
    recipe_category.save_mysql_recipe()