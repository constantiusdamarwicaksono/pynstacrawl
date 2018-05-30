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
	      echo 'Building crawler'
      }
    }
    stage('Test') {
      parallel{
        stage('API Testing'){
          steps{
            echo "Running api testing"
          }
        }
        stage('Unit Testing'){
          steps{
            echo "Running Unit Testing"
          }
        }
        stage('UI Testing'){
          steps{
            echo "Running UI Testing"
          }
        }
      }
    }
    stage('Result') {
      steps {
        echo 'Publishing Result'
      }
    }
  }
}
