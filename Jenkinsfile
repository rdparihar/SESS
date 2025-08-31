pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'cd sess_dev && python manage.py test'
            }
        }
    }
}
