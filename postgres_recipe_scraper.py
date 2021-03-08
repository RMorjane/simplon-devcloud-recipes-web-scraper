import requests
import pprint
import psycopg2
from bs4 import BeautifulSoup
import logging    
from logging.handlers import RotatingFileHandler

class RecipeCategory:

    def __init__(self,url):
        self.url = url
        self.recipe_category_name = ""
        self.links = []

    def read_infos(self):
        response = requests.get(self.url)
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, from_encoding=encoding,features="html.parser")
        self.recipe_category_name = " ".join(soup.find("h1").string.split())
        self.links = [
            {
                "recipe_name": loop_link["title"],
                "href": loop_link["href"]
            }
            for loop_link in soup.find_all("a",{"class": "recipe-name"},href=True)        
        ]

    def display(self):
        print("%s : " %self.recipe_category_name)
        for loop_link in self.links:
            print(loop_link)

    def save_mysql_recipe(self):
        mysql_recipe = MySQLRecipe()
        mysql_recipe.set_logger()
        if mysql_recipe.connect() and mysql_recipe.create_database():
            for loop_link in self.links:
                print(loop_link["href"])
                recipe_info = RecipeInfo(loop_link["href"],mysql_recipe)
                recipe_info.read_infos()
            mysql_recipe.connection.close()

class RecipeInfo:

    def __init__(self,href,mysql_recipe):
        self.recipe_url = "https://www.atelierdeschefs.fr" + href
        self.recipe_name = ""
	self.recipe_image = ""
        self.persons_count = 0
        self.list_usages = []
        self.list_ingredients = []
        self.list_steps = []
        self.mysql_recipe = mysql_recipe

    def read_infos(self):
        response = requests.get(self.recipe_url)
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, from_encoding=encoding,features="html.parser")
        self.recipe_name = soup.find("h1").string

        try:
            image = soup.find("img",{"class": "image-resize lazy"})
            self.recipe_image = image["data-src"]
        except:
            image = soup.find("img",{"class": "lazy"})
            self.recipe_image = image["data-src"]
        print(self.recipe_image)

        self.persons_count = int(soup.find("option",{"class": "yield"}).string)
        self.list_usages = [loop_usage.string for loop_usage in soup.find_all("li",{"class": "bold marginT10"})]

        if self.mysql_recipe.connection:
            sql_recipe_id = self.mysql_recipe.get_recipe_id(self.recipe_name)
            recipe_id = 0
            if sql_recipe_id and type(sql_recipe_id)==tuple:
                recipe_id = sql_recipe_id[0]
                print(recipe_id," : ",self.recipe_name," already exists")
            else:
                recipe_id = self.mysql_recipe.add_recipe(self.recipe_name,self.recipe_url)

                usage = "ingredient"
		list_li = soup.find_all("li")
                for k in list_li:
                    k_childs = k.findChildren()
                    if len(k_childs)==2 and k_childs[0].name=="span" and k_childs[1].name=="span":
                        final_index = len(k_childs[0].text)-3
                        list_quantity = k_childs[1].text.split(' ')

                        usage_id = mysql_recipe.add_ingredient_usage(usage)

                        ingredient = " ".join(k_childs[0].text.strip()[0:final_index].split())
                        ingredient_id = mysql_recipe.add_ingredient(ingredient)

                        try:
                            quantity = int(list_quantity[0])
                        except:
                            quantity = float(list_quantity[0])

                        unit = list_quantity[1]

                        self.mysql_recipe.add_recipe_ingredient(recipe_id,ingredient_id,usage_id,self.persons_count,quantity,unit)

                        self.list_ingredients.append(
                            {
                                "usage": usage,
                                "persons_count": self.persons_count,
                                "ingredient": ingredient,
                                "quantity": quantity,
                                "unit": unit
                            }
                        )

                    elif k.text in self.list_usages:
                        usage = k.text

                steps_name = [step.string for step in soup.find_all("span",{"class": "bold"}) if ". POUR " in step.string]
                steps_description = soup.find_all("p",{"class": "marginT10 fz110 lh120"})
                steps_count = len(steps_name)
                for i in range(steps_count):
                    order = steps_name[i]
                    description = steps_description[i].text.replace("\r\n"," ").replace("\n","")

                    self.mysql_recipe.add_step_recipe(recipe_id,order,description)
                        
                    self.list_steps.append(
                        {
                            "order": order,
                            "description": description
                        }
                    )

    def display(self):
        print(self.recipe_name)
        pprint.pprint(self.list_ingredients)
        pprint.pprint(self.list_steps)

class MySQLRecipe:

    def __init__(self):
        self.connection = None
        self.logger = None
        self.list_recipes = []

    def connect(self):
        try:
            cnt_string = f"host=simplon-morjane-recipes.postgres.database.azure.com user=mrhellab@simplon-morjane-recipes dbname=postgres password=Oumaima1* sslmode='require'"
            self.connection = psycopg2.connect(cnt_string)
            print("Connexion réussie : " + str(self.connection))
            return True
        except (Exception, psycopg2.Error) as error:
            print("Impossible de se connecter au serveur postgres : " + str(error))
            return False

    def create_database(self):
        try:
            with self.connection.cursor() as my_cursor:
                sql_create_tables = """
                    CREATE SCHEMA myrecipes;

                    CREATE TABLE recipe(
                        recipe_id SERIAL,
                        recipe_name VARCHAR(100) not null,
                        recipe_url VARCHAR(200) not null
                    );

                    CREATE TABLE ingredient(
                        ingredient_id SERIAL,
                        ingredient_name VARCHAR(50) NOT NULL
                    );

                    CREATE TABLE ingredient_usage(
                        usage_id SERIAL,
                        usage_name VARCHAR(50) not null
                    );

                    CREATE TABLE recipe_ingredient(
                        recipe_id INT NOT NULL,
                        ingredient_id INT NOT NULL,
                        usage_id INT NOT NULL,
                        persons_count INT NOT NULL,
                        quantity INT NOT NULL,
                        unit VARCHAR(20) NOT NULL,
                        PRIMARY KEY(recipe_id,ingredient_id,usage_id,persons_count)
                    );

                    CREATE TABLE step_recipe(
                        step_name VARCHAR(50) NOT NULL,
                        recipe_id INT NOT NULL,
                        step_description TEXT,
                        PRIMARY KEY(step_name,recipe_id)
                    );
                """
                my_cursor.execute(sql_create_tables)
                my_cursor.close()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Impossible de créer les tables au niveau du serveur postgres : " + str(error))
            self.connection.close()
            return False

    def add_ingredient(self,ingredient_name):
        ingredient_id = 0
        sql_ingredient_id = self.get_ingredient_id(ingredient_name)
        print("ingredient id : ",sql_ingredient_id)
        if sql_ingredient_id and type(sql_ingredient_id)==tuple:
            ingredient_id = sql_ingredient_id[0]
        else:
            with self.connection.cursor() as my_cursor:
                sql_add_ingredient = "INSERT INTO ingredient(ingredient_name) VALUES(%s)"
                my_cursor.execute(sql_add_ingredient,(ingredient_name,))
                self.connection.commit()
                my_cursor.close()
                ingredient_id = self.get_ingredient_id(ingredient_name)
        return ingredient_id

    def get_ingredient_id(self,ingredient_name):
        with self.connection.cursor() as my_cursor:
            sql_ingredient_id = "SELECT ingredient_id FROM ingredient WHERE ingredient_name=%s"
            my_cursor.execute(sql_ingredient_id,(ingredient_name.replace("'","\'"),))
            ingredient_id = my_cursor.fetchone()
            my_cursor.close()
            return ingredient_id

    def add_ingredient_usage(self,usage_name):
        usage_id = 0
        sql_usage_id = self.get_usage_id(usage_name)
        print("usage id : ",sql_usage_id)
        if sql_usage_id and type(sql_usage_id)==tuple:
            usage_id = sql_usage_id[0]
        else:
            with self.connection.cursor() as my_cursor:
                sql_add_usage = "INSERT INTO ingredient_usage(usage_name) VALUES(%s)"
                my_cursor.execute(sql_add_usage,(usage_name,))
                self.connection.commit()
                my_cursor.close()
                usage_id = self.get_usage_id(usage_name)
        return usage_id

    def get_usage_id(self,usage_name):
        with self.connection.cursor() as my_cursor:
            sql_usage_id = "SELECT usage_id FROM ingredient_usage WHERE usage_name=%s"
            my_cursor.execute(sql_usage_id,(usage_name.replace("'","\'"),))
            usage_id = my_cursor.fetchone()
            my_cursor.close()
            return usage_id

    def add_recipe(self, recipe_name, recipe_url, recipe_image):
        with self.connection.cursor() as my_cursor:
            sql_add_recipe = "INSERT INTO recipe(recipe_name,recipe_url,recipe_image) VALUES('{0}','{1}','{2}')".format(
                recipe_name,recipe_url)
            my_cursor.execute(sql_add_recipe)
            self.connection.commit()
            my_cursor.close()
            recipe_id = self.get_recipe_id(recipe_name)
            return recipe_id       

    def get_recipe_id(self,recipe_name):
        with self.connection.cursor() as my_cursor:
            sql_recipe_id = "SELECT recipe_id FROM recipe WHERE recipe_name=%s"
            my_cursor.execute(sql_recipe_id,(recipe_name.replace("'","\'"),))
            recipe_id = my_cursor.fetchone()
            my_cursor.close()
            return recipe_id

    def add_recipe_ingredient(self,recipe_id,ingredient_id,usage_id,persons_count,quantity,unit):
        recipe_ingredient_id = None
        with self.connection.cursor() as my_cursor:
            sql_add_recipe_ingredient = """
                INSERT INTO recipe_ingredient(
                    recipe_id,ingredient_id,usage_id,persons_count,quantity,unit)
                VALUES(%s,%s,%s,%s,%s,%s)
            """
            my_cursor.execute(
                sql_add_recipe_ingredient,
                (recipe_id,ingredient_id,usage_id,persons_count,quantity,unit)
            )
            self.connection.commit()
            recipe_ingredient_id = my_cursor.lastrowid
            my_cursor.close()
        return recipe_ingredient_id

    def add_step_recipe(self,recipe_id,order,description):
        step_recipe_id = None
        with self.connection.cursor() as my_cursor:
            sql_add_step = """
                INSERT INTO step_recipe(step_name,recipe_id,step_description) VALUES(%s,%s,%s)
            """
            my_cursor.execute(
                sql_add_step,(order.replace("'","\'"),recipe_id,description.replace("'","\'"))
            )
            self.connection.commit()
            step_recipe_id = my_cursor.lastrowid
            my_cursor.close()
        return step_recipe_id

    def find_recipes(self,recipe_dict={}):
        list_keys = []
        list_values = []
        list_args = ()
        for key,value in recipe_dict.items():
            list_keys.append(key)
            list_values.append(value)
        try:
            with self.connection.cursor() as my_cursor:
                sql_find_recipes = "SELECT * FROM recipe"
                for i in range(len(list_keys)):
                    if i==0:
                        sql_find_recipes += " WHERE "
                    else:
                        sql_find_recipes += " AND "
                    if type(list_values[i])==str:
                        list_args = (list_args + ("%"+list_values[i]+"%",))
                        sql_find_recipes += list_keys[i] + " LIKE '%s'"
                    elif type(list_values[i])==int:
                        list_args = (list_args + (list_values[i],))
                        sql_find_recipes += list_keys[i] + "=%s"
                print(sql_find_recipes)
                my_cursor.execute(sql_find_recipes %(list_args))
                self.list_recipes = []
                for recipe in my_cursor.fetchall():
                    self.list_recipes.append({
                        "recipe_id": recipe[0],
                        "recipe_name": recipe[1],
                        "recipe_url": recipe[2],
                    })
                my_cursor.close()
                self.logger.info("Successfull : Recipes was founded")
        except (Exception, psycopg2.Error) as error:
            self.logger.error("Erreur dans la requête de selection des recettes : "+str(error))

    def set_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)        
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('log.txt', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)