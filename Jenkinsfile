pipeline {
  agent any
  stages {
    stage('init') {
      steps {
        sh '''#!/bin/bash

sudo curl -L https://github.com/docker/compose/releases/download/1.11.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose up'''
      }
    }
  }
}