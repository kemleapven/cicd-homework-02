pipeline {
    agent any

    environment {
        // Docker Hub repository and image settings
        DOCKER_IMAGE = 'kemleapx20/cicd-web-app'
        IMAGE_TAG    = "${BUILD_NUMBER}"
        STACK_NAME   = 'cicd-homework'
    }

    stages {
        stage('Lint & Unit Test') {
            steps {
                echo '=== Stage: Running Tests ==='
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m pip install --quiet -r requirements.txt
                            python3 -m pytest test_app.py -v
                        '''
                    } else {
                        bat '''
                            python -m pip install --quiet -r requirements.txt
                            python -m pytest test_app.py -v
                        '''
                    }
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "=== Stage: Building Docker Image ${DOCKER_IMAGE}:${IMAGE_TAG} ==="
                script {
                    if (isUnix()) {
                        sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest ."
                    } else {
                        bat "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest ."
                    }
                }
            }
        }

        stage('Docker Push') {
            steps {
                echo "=== Stage: Pushing Image to Docker Hub ==="
                script {
                    try {
                        if (isUnix()) {
                            sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                            sh "docker push ${DOCKER_IMAGE}:latest"
                        } else {
                            bat "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                            bat "docker push ${DOCKER_IMAGE}:latest"
                        }
                    } catch (Exception e) {
                        echo "Docker Hub push notification: ${e.message}"
                        echo "Proceeding with deployment..."
                    }
                }
            }
        }

        stage('Deploy to Docker Swarm') {
            steps {
                echo "=== Stage: Deploying Stack '${STACK_NAME}' via Docker Swarm ==="
                script {
                    if (isUnix()) {
                        sh """
                            docker stack deploy -c docker-stack.yml ${STACK_NAME}
                            docker stack services ${STACK_NAME}
                        """
                    } else {
                        bat """
                            docker stack deploy -c docker-stack.yml ${STACK_NAME}
                            docker stack services ${STACK_NAME}
                        """
                    }
                }
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
