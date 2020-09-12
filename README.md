# lending-service

## Description

Service de gestion des livres empruntés
  
## Fonctionnalitées  

* **Get expired books** : Renvoie la liste des livres empruntés dont la date de retour est dépassée, avec le nom de l'utilisateur et son adresse email
* **Save lend** : Ajoute dans la base de donnée un livre emprunté avec le nom de l'utilisateur, son adresse mail et la date d'emprunt
* **Delete book** : Supprime une entrée dans la base

## Technologie

Le service est développé en java et utilise le framework [Spring Boot](https://spring.io/projects/spring-boot)  
Les données sont stockées dans une base de donnée mySQL

## Base de données

La base de données contient tous les livres empruntés sous la forme *id, titre du livre, utilisateur, adresse mail, date d'emprunt*  
Une fois que la date d'emprunt est dépassée de 30 jours, toute, les indormations sont fournis via la requête **get expired books**

## Requêtes d'envoi d'un emprunt
    curl -X POST -H "Content-type: application/json" -d '{"book":"NOM_DU_LIVRE","name":"NOM","email":"EMAIL"}'http://localhost:8080/saveLend

## Requêtes d'envoi d'un retour
    curl -X POST -H "Content-type: application/json" -d '{"book" : "Nom_du_livre" }' http://localhost:8080/deleteBook

## Requêtes d'envoi des livres non retournés
    http://localhost:8080/getBookExpired

## Commande de lancement du docker
	docker run -e MYSSQL_DB_HOST=jdbc:mysql://192.168.56.1:3306/books_lend?serverTimezone=UTC -e MYSQL_DB_USERNAME=root -e MYSQL_DB_PASSWORD=root lending-service

## Equipe

Lucas Greck, Bastien Gucciardo et Nicolas Petit
