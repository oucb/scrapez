# ScrapEZ

**ScrapEZ** est une application web pour 'scraper' (parcourir) des sites internets:

* Rechercher et télécharger des fichiers de n'importe quelle extension (pdf, xml, png, mp4, ...)
* Rechercher et télécharger des videos et de la musique de n'importe quelle plaforme (YouTube, Vimeo, VK, Spotify, Deezer, ...)
* Organiser les fichiers par section Music, Documents, Videos, et Liens.
* Visualiser et catégoriser les marques pages et les liens.
* Backup les données localement ou sur le cloud.

## Installation

### Récupérer le code de ScrapEZ
  ```
  git clone https://github.com/ocervell/scrapez.git
  ```
  
### Créer un environment virtuel avec virtualenv
  ```
  cd scrapez
  pip install virtualenv
  virtualenv venv/
  source venv/bin/activate
  ```
  **Note:** Sur Windows, `bin/` est remplacé par `Scripts/`, la dernière ligne devient: `source venv/Scripts/activate`
  
### Installer les packages dont ScrapEZ a besoin
  ```
  pip install -r requirements.txt
  ```
  
### Installer Redis
  
  ```
  brew install redis
  ```
  
  **Pour Windows**, suivre les [instructions d'installation](https://github.com/rgl/redis/downloads)
  
## Execution

### Démarrer Redis

  **Pour Mac**, entrer:
  ```
  redis-server
  ```
  
  **Pour Windows**, vérifier que le service "Redis Server" est lancé (click droit - Démarrer):
  ![](https://user-images.githubusercontent.com/9629314/34919199-f81d5268-f924-11e7-8d3c-faffd8ce1dfd.PNG)

### Démarrer l'interface web de ScrapEZ**
 ```
  python manage.py runserver --threaded -d -r
  >> App running on 5000 ...
  ```
### Démarrer l'éxecuteur de ScrapEZ (Celery)**
  ```
  celery worker -A celeryapp.app -l info -P eventlet
  ```
  
  * L'éxecuteur a pour charge d'exécuter des fonctions qui seraient trop longues dans le contexte d'une requête HTTP (qui possède un timeout et n'est donc pas approprié pour des fonctions lourdes).
  
  * L'interface web créee des tâches (`tasks`) et les met dans la file (Redis). 
  
  * L'éxecuteur récupère les tâches de la liste et les éxecute.
  
## Scrape !
* Visiter `localhost:5000/videos`
* Faites une recherche
