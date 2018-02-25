pipeline {
  agent any
  stages {
    stage('init') {
      steps {
        sh '''#!/bin/bash

yum groupinstall "Development Tools"
pip install -r requirements.txt
pip install -e .
FLASK_APP=scrapez/ui/app.py flask run'''
      }
    }
  }
}