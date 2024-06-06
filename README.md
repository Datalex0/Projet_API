# Projet développement d'une API

## Collaborateurs:
- Kévin Perquy
- Alexis Murail
- Luis-Miguel Borderon
- Florence Bouchart

## Prérequis :
- MariaDB community 11.3 (ou MySQL)
- IDE installé sur la machine
- Postman installé sur la machine _(optionnel pour les tests)_
- Dbeaver ou Extension MySQL installé sur la machine
- Python 3.11
- Installation du requirement.txt

## Utilisation de l'API : 
1. Créer une base de données MySQL via MariaDB
2. Télécharger le dossier Projet_API en entier
3. Ouvrir le dossier dans VScode ou un autre IDE
4. Dans le dossier database, ouvrir database.py et remplacer l'url par celui de votre base de données :
   ```SQLALCHEMY_DATABASE_URL = "url_de_votre_base_de_données"```
5. Exécuter le fichier main.py

## Lancement de Swagger : 
**ATTENTION** : Impossibilité de lancer Swagger et l'API en simultanée.

Pour lancer Swagger et l'API en même temps, modifier le port dans server.py

1. Aller jusqu'à l'étape 4 puis lancer server.py 
2. Connexion à l'API Swagger : [http://localhost:5000/api/ui/](http://localhost:5000/api/ui/)

## Vous trouverez : 
- [Documentation technique]()
