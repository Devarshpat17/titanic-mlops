pipeline {
    agent any

    environment {
        REPO = 'https://github.com/Devarshpat17/titanic-mlops.git'
    }

    stages {
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
    }

    post {
        always {
            echo 'Tearing down containers...'
            sh 'docker-compose down || true'
        }
    }
}
