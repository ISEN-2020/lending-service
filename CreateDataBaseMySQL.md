# How to create the lending-service MySQL DataBase

## Create the DataBase
	CREATE DATABASE book_lend;

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