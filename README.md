# Web Recipe Scraper

Web Recipe Scraper is a web application witch get recipes data from the web site : https://atelierdeschefs.fr and display recipes you want to find depending on search criteria.

Just type criteria on search bar.

when you click on recipe item, it redirect you on recipe's web details.

![image](https://user-images.githubusercontent.com/71873995/110260197-81dfe000-7fab-11eb-996b-48ec73a1117c.png)

![image](https://user-images.githubusercontent.com/71873995/110260256-a76ce980-7fab-11eb-9970-d3c8345cc6c2.png)


## Installation

docker-compose file : 
````
version: "3.1"

services:

  db:
    container_name: mysql_db
    image: mysql:8.0.21
    restart: always
    env_file: env
    networks: 
      - myrecipes
  
  flask_app:
    container_name: mysql_flask
    build: ./app
    depends_on: 
      - db   
    ports:
      - 4001:3001
    volumes:
      - .:/app
    networks:
      - myrecipes
    command: sh -c "python main.py"

networks: 
  myrecipes: {}`
````

Use the following command line :

```bash
docker-compose up --build
```

## Technologies

#### Back-End :
``
Python : language for loading the recipe scraper,
Flask : creating recipe web application,
Jinja2 : transfering data from Back to Front,
render_template : rendering the web page
``
#### Front-End :
``
HTML5,
CSS3,
Javascript
``


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
