drop database if exists recipes;
create database if not exists recipes;
use recipes;

create table recipe(
	recipe_id int auto_increment,
    	recipe_name varchar(100) not null,
    	recipe_url varchar(200) not null,
	recipe_image varchar(200) not null,	
    	primary key(recipe_id)
);

create table ingredient(
	ingredient_id int not null auto_increment,
    	ingredient_name varchar(50) not null,
    	primary key(ingredient_id)
);

create table ingredient_usage(
	usage_id int not null auto_increment,
	usage_name varchar(50) not null,
	primary key(usage_id)
);

create table recipe_ingredient(
	recipe_id int not null,
    	ingredient_id int not null,
	usage_id int not null,
    	persons_count int not null,
    	quantity int not null,
    	unit varchar(20) not null,
    	primary key(recipe_id,ingredient_id,usage_id,persons_count)
);

create table step_recipe(
	step_name varchar(50) not null,
    	recipe_id int not null,
    	step_description longtext,
    	primary key(step_name,recipe_id)
);