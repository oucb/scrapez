pipeline {
  agent any
  stages {
    stage('init') {
      steps {
        sh '''#!/bin/bash

echo "Running as `whoami`"
sudo apt-get install -y python-pip python-virtualenv
virtualenv venv
venv/bin/pip install flask
venv/bin/pip install -r requirements.txt
venv/bin/pip install -e .
FLASK_APP=scrapez/ui/app.py venv/bin/flask run'''
      }
    }
  }
}