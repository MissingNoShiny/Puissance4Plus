# Puissance4Plus

## Prérequis

Le jeu a été développé en utilisant Flask, un framework de développement web en python. 
Il faut donc avoir installé python pour le faire tourner. 
Nous avons utilisé la version 3.7 lors du développement, 
mais le jeu devrait également fonctionner avec la version 3.6 
(pas en dessous cependant, en raison de l’utilisation de f-strings).

Les bibliothèques supplémentaires nécessaires à l’exécution sont listées dans `requirements.txt` à la racine du projet.
Elles peuvent être installées automatiquement à l'aide de la commande `pip install -r requirements.txt`.

## Lancer l'application

### À partir de main.py

Depuis la racine du projet, effectuer la commande `python main.py`.

### En générant le .exe

Il est également possible de générer un .exe grâce à PyInstaller. 
Il suffit pour ce faire de double cliquer sur le fichier `installer.bat` présent à la racine du projet. 
Ce .exe peut ensuite être placé n’importe où sur l’ordinateur, et même être distribué à d’autres personnes, 
qui n’auront normalement pas à installer python ni les bibliothèques.