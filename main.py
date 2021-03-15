import logging
from mysql_recipe_scraper import RecipeCategory, MySQLRecipe
from flask import Flask, render_template, request

logging.basicConfig(filename='logs.log', level=logging.DEBUG)

app = Flask(__name__)

scraping = False
cnt = MySQLRecipe()
cnt.set_logger()
cnt.connect()

@app.route("/", methods=['GET'])
def display_recipes():
    list_recipes = []
    recipe = request.args.get("recipe")
    if recipe == None:
        cnt.find_recipes()
    else:
        try:
            recipe_id = int(recipe)
            cnt.find_recipes({
                "recipe_id": recipe_id
            })
        except:
            recipe_name = str(recipe)
            cnt.find_recipes({
                "recipe_name": recipe_name
            })
    list_recipes = cnt.list_recipes
    return render_template("index.html", recipes=list_recipes)

if __name__ == '__main__':

    url_recipes = "https://www.atelierdeschefs.fr/fr/recettes-de-crepes-au-chocolat.php"
    recipe_category = RecipeCategory(url_recipes)
    recipe_category.read_infos()
    recipe_category.display()
    recipe_category.save_mysql_recipe()

    app.run(host="0.0.0.0", port=3000, debug=True)
