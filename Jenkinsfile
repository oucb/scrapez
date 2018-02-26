pipeline {
  agent any
  stages {
    stage('init') {
      steps {
        sh '''sudo /usr/local/bin/docker-compose up'''
      }
    }
  }
}
