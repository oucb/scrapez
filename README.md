# ScrapEZ

ScrapEZ is a web application to scrape websites for files that you are interested in.

* Search and download files from any extension format (pdf, xml, png, css, html, js, ...).
* Search and download videos and music from popular platforms (YouTube, Vimeo, VK, Spotify, Deezer, Dailymotion, Pandora, ...).
* Music, Documents and Videos organized
* Bookmarks visualization to categorize links
* Files downloaded locally automatically

## Install

* **Install ScrapEZ**
  ```
  git clone https://github.com/ocervell/scrapez.git
  pip install -r requirements.txt
  ```
  
* **Install Redis**
  
  **On Mac**, make sure you have [XCode](https://itunes.apple.com/us/app/xcode/id497799835?mt=12), [Macports](https://guide.macports.org/chunked/installing.macports.html) and [Brew](https://brew.sh/) installed, and run:
  ```
  brew install redis
  ```
  
  **On Windows**, follow the [installation instructions](https://github.com/rgl/redis/downloads)
  
## Run

* **Run Redis**

  **On Mac**, run:
  ```
  redis-server
  ```
  
  **On Windows**, verify that "Redis Server" service is running (right click -> Start):
  ![](https://user-images.githubusercontent.com/9629314/34919199-f81d5268-f924-11e7-8d3c-faffd8ce1dfd.PNG)

* **Run ScrapEZ UI**
  ```
  python manage.py runserver --threaded -d -r
  >> App running on 5000 ...
  ```
* **Run ScrapEZ Celery worker**
  ```
  celery worker -A celeryapp.app -l info -P eventlet
  ```

## Scrape !
* Visit `localhost:5000`
* Enter a URL in the search box
* Enter a list of extensions to search for
* Click 'Scrape it !'
