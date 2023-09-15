# This step is useless if Docker is started with docker-compose

# How to create the lending-service MySQL DataBase

## Create the DataBase
	CREATE DATABASE books_lend;

## Create the Table
	CREATE TABLE books (
  		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  		book VARCHAR(100) NOT NULL,
  		name VARCHAR(40) NOT NULL,
  		email VARCHAR(40) NOT NULL,
  		date DATE NOT NULL,
  		PRIMARY KEY (id)
  		)
  		ENGINE=INNODB;

## Add an expired book in the database
  	INSERT INTO books (book,name,email,date) VALUES ('Le JAVA pour les GROS nuls', 'Sigalas', 'florian.sigalas@isen.yncrea.fr', '2020-07-05');
