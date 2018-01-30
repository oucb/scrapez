# ScrapEZ

**ScrapEZ** is a web application to scrape websites for files that you are interested in.

* Search and download files from any extension format (pdf, xml, png, css, html, js, ...).
* Search and download videos and music from popular platforms (YouTube, Vimeo, VK, Spotify, Deezer, Dailymotion, Pandora, ...).
* Organize scraped Music, Documents, Videos and Links.
* Visualize and categorize Bookmarks and Links.
* Backup scraped data locally or on the cloud.

## Quickstart (Docker)
You'll need to have `docker` and `docker-compose` installed.
```
# Get the code
git clone https://github.com/ocervell/scrapez.git

# Go to the code folder
cd scrapez

# Bring up the services
docker-compose up
```

* Run in the background by using `docker-compose up -d` (detached).
* Check the UI is running by navigating to `localhost:5000`.
* Tail the logs by using `docker-compose logs -f`.

**Note:** If you get a "version unsupported" error, you need to upgrade `docker-compose`:
```
sudo rm /usr/bin/docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.11.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Quickstart (supervisor)
Let's clone the repo, create a virtualenv, install the pip requirements and run our application.

In a terminal (Ubuntu here):

```
# Get the code
git clone https://github.com/xavierfav/meloshare

# Create virtualenv
mkvirtualenv meloshare # Note: You can also use the command `virtualenv venv`.

# Install pip dependencies
pip install -r requirements.txt 

# Install Redis
apt install redis-server 

# Run supervisor
supervisord -c supervisord.conf # run all services

# Administrate services (stop, start, restart, reload, ...)
supervisorctl 
```

After running the above steps the following services should be RUNNING in `supervisorctl` shell:
- `ui`  --> User interface (port 5000)
- `api` --> Application programming interface (port 5001)
- `worker` --> Celery worker processing tasks
- `scheduler` --> Celery scheduler for periodic tasks
- `redis` --> Redis server (API caching for GET requests)

Supervisor allows you to administrate the services from the shell with the commands: `status <service>`, `start <service>`, `stop <service>`, `restart <service>`, or `tail -f <service>`.

You can also use `start/stop/status all` to control all services.

You can pass a space-separated list of services to control multiple simultaneously.

You can reload the supervisor configuration and update the running processes: `reread` and then `update`.

## Scrape !
* Visit `localhost:5000`
* Enter a URL in the search box
* Enter a list of extensions to search for
* Click 'Scrape it !'

## Development

Supervisor is merely running commands for you and control the life of your processes.
The following shows which command is run by supervisor for each service.

### Get the code
  ```
  git clone https://github.com/ocervell/scrapez.git
  ```
  
### Create virtualenv
  ```
  cd scrapez
  pip install virtualenv
  virtualenv venv/
  source venv/bin/activate
  ```
  **Note:** 
  
   On Windows, you'll need to install Cygwin to execute the steps above and run `scrapez`.
   On Windows, `bin/` is replaced by `Scripts/`, the last line becomes: `source venv/Scripts/activate`
  
### Install ScrapEZ requirements
  ```
  pip install -r requirements.txt
  ```
  
### Install Redis
  
  **On Mac**, make sure you have [XCode](https://itunes.apple.com/us/app/xcode/id497799835?mt=12), [Macports](https://guide.macports.org/chunked/installing.macports.html) and [Brew](https://brew.sh/) installed, and run:
  ```
  brew install redis
  ```
  
  **On Windows**, follow the [installation instructions](https://github.com/rgl/redis/downloads)
  
### Run Redis
```
redis-server
```

### Run the UI
  ```
  FLASK_APP=scrapez/ui/app.py flask run  --host 0.0.0.0 --port 5000
  >> Running on port 5000 ...
  ```
  
### Run the API
  ```
  FLASK_APP=scrapez/api/app.py flask run --host 0.0.0.0 --port 5001
  >> Running on port 5001 ...
  ```

### Run the worker
```
celery worker -A scrapez.celeryapp:app -l info
```
