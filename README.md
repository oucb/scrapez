# ScrapEZ

ScrapEZ is a web application to scrape websites for files that you are interested in.

It allows to search and download files from any extension format (pdf, xml, png, css, html, js, ...).

## Install

* Install ScrapEZ
  ```
  git clone https://github.com/ocervell/scrapez.git
  pip install -r requirements.txt
  ```
  
* Install Redis
  ```
  brew install redis
  ```

## Run

* Run Redis
  ```
  redis-server
  ```
  
* Run ScrapEZ
  ```
  python app.py
  >> App running on 5000 ...
  ```
* Run ScrapEZ Celery worker
  ```
  celery worker -A celeryapp.app -l info -P eventlet
  ```

## Scrape !
* Visit `localhost:5000`
* Enter a URL in the search box
* Enter a list of extensions to search for
* Click 'Scrape it !'
