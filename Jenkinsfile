pipeline {
  agent any
  stages {
    stage('Preparation') {
      parallel {
        stage('Preparation') {
          steps {
            echo 'First Preparation'
          }
        }
        stage('Preparation 2') {
          steps {
            echo 'Second Preparation'
          }
        }
      }
    }
    stage('Build') {
      steps {
        echo 'In Build Step'
      }
    }
    stage('Test') {
      steps {
        echo 'In test Step'
      }
    }
    stage('Result') {
      steps {
        echo 'Publishing Result'
      }
    }
  }
}
