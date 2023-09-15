	CREATE DATABASE IF NOT EXISTS books_lend;
	CREATE TABLE IF NOT EXISTS books (
  		id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  		book VARCHAR(100) NOT NULL,
  		name VARCHAR(40) NOT NULL,
  		email VARCHAR(40) NOT NULL,
  		date DATE NOT NULL,
        quantites SMALLINT NOT NULL,
  		PRIMARY KEY (id)
  		)
  		ENGINE=INNODB;
  	INSERT INTO books (book,name,email,date) VALUES ('Le JAVA pour les GROS nuls', 'Sigalas', 'florian.sigalas@isen.yncrea.fr', '2020-07-05');