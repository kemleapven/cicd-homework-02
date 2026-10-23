pipeline {
    agent any

    environment {
        // Docker Hub repository and image settings
        DOCKER_IMAGE   = 'kemleapx20/cicd-web-app'
        IMAGE_TAG      = "${BUILD_NUMBER}"
        STACK_NAME     = 'cicd-homework'
        // Docker Hub Credentials ID configured in Jenkins (Manage Jenkins -> Credentials)
        DOCKER_HUB_CREDS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '=== Stage: Checkout Source Code ==='
                checkout scm
            }
        }

        stage('Lint & Unit Test') {
            steps {
                echo '=== Stage: Running Tests ==='
                // Runs unit tests inside python environment or container
                sh '''
                    python3 -m pip install --quiet --upgrade pip
                    python3 -m pip install --quiet -r requirements.txt
                    python3 -m pytest test_app.py -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo "=== Stage: Building Docker Image ${DOCKER_IMAGE}:${IMAGE_TAG} ==="
                sh """
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Docker Push') {
            steps {
                echo "=== Stage: Pushing Image to Docker Hub ==="
                // If credentials are configured in Jenkins:
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: env.DOCKER_HUB_CREDS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh """
                                echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                                docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                                docker push ${DOCKER_IMAGE}:latest
                            """
                        }
                    } catch (Exception e) {
                        echo "Docker Hub credentials not configured or push failed: ${e.message}"
                        echo "Skipping push or proceeding with locally built image..."
                    }
                }
            }
        }

        stage('Deploy to Docker Swarm') {
            steps {
                echo "=== Stage: Deploying Stack '${STACK_NAME}' via Docker Swarm ==="
                sh """
                    docker stack deploy -c docker-stack.yml ${STACK_NAME}
                    docker stack services ${STACK_NAME}
                """
            }
        }
    }

    post {
        always {
            echo 'CI/CD Pipeline finished.'
        }
        success {
            echo 'Pipeline completed successfully! Microservice deployed.'
        }
        failure {
            echo 'Pipeline failed. Please check build logs above for troubleshooting.'
        }
    }
}
