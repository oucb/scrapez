pipeline {
  agent any
  stages {
    stage('init') {
      steps {
        sh '''#!/bin/bash

echo "Running as `whoami`"
sudo apt-get install -y python-pip python-virtualenv
pip install flask
pip install -r requirements.txt
pip install -e .
FLASK_APP=scrapez/ui/app.py venv/bin/flask run'''
      }
    }
  }
}