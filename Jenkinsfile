pipeline {
  agent any
  stages {
    stage('error') {
      steps {
        sh '''#!/bin/bash

sudo apt-get install python-pip
pip install -r requirements.txt
pip install -e .
FLASK_APP=scrapez/ui/app.py flask run'''
      }
    }
  }
}