pipeline {
  agent any
  stages {
    stage('') {
      steps {
        sh '''#!/bin/bash

pip install -r requirements.txt
pip install -e .
FLASK_APP=scrapez/ui/app.py flask run'''
      }
    }
  }
}