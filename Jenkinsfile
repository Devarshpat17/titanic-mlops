pipeline {
    agent any
    environment {
        REPO = 'https://github.com/yourusername/titanic-mlops.git' // REPLACE with your repo
    }
    stages {
        stage('Checkout') {
            steps {
                git url: env.REPO
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Up') {
            steps {
                sh 'docker-compose up -d'
            }
        }
        stage('Smoke Tests') {
            steps {
                sh 'sleep 8'
                sh 'curl -f http://localhost:5000 || (echo "Webapp not responding"; exit 1)'
                sh 'curl -f http://localhost:5001/records || (echo "DBapp not responding"; exit 1)'
            }
        }
        stage('Teardown') {
            steps {
                sh 'docker-compose down'
            }
        }
    }
}
