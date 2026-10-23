pipeline {
    agent any

    environment {
        // Application and Registry settings
        IMAGE_NAME        = 'kemleapx20/cicd-web-app'
        IMAGE_TAG         = "${BUILD_NUMBER}"
        STACK_NAME        = 'cicd-homework'
        
        // AWS ECR Configuration
        AWS_REGION        = 'ap-southeast-1'
        AWS_ACCOUNT_ID    = 'YOUR_AWS_ACCOUNT_ID'
        ECR_REPO          = 'cicd-web-app'
        ECR_URI           = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"
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
                echo "=== Stage: Building Docker Image ${IMAGE_NAME}:${IMAGE_TAG} ==="
                script {
                    if (isUnix()) {
                        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                    } else {
                        bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                    }
                }
            }
        }

        stage('Docker Registry Push') {
            steps {
                echo "=== Stage: Pushing Images to Registry (Amazon ECR / Docker Hub) ==="
                script {
                    // 1. Attempt AWS ECR Login & Push if AWS CLI & Account are configured
                    try {
                        echo "Authenticating to Amazon ECR (${AWS_REGION})..."
                        if (isUnix()) {
                            sh """
                                if which aws > /dev/null 2>&1 && [ "${AWS_ACCOUNT_ID}" != "YOUR_AWS_ACCOUNT_ID" ]; then
                                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
                                    docker tag ${IMAGE_NAME}:latest ${ECR_URI}:latest
                                    docker push ${ECR_URI}:${IMAGE_TAG}
                                    docker push ${ECR_URI}:latest
                                    echo "Successfully pushed to Amazon ECR: ${ECR_URI}:${IMAGE_TAG}"
                                else
                                    echo "AWS CLI or Account ID not set; skipping ECR push."
                                fi
                            """
                        } else {
                            bat """
                                @echo off
                                where aws >nul 2>nul
                                if %ERRORLEVEL% EQU 0 (
                                    if not "${AWS_ACCOUNT_ID}"=="YOUR_AWS_ACCOUNT_ID" (
                                        aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com
                                        docker tag %IMAGE_NAME%:%IMAGE_TAG% %ECR_URI%:%IMAGE_TAG%
                                        docker tag %IMAGE_NAME%:latest %ECR_URI%:latest
                                        docker push %ECR_URI%:%IMAGE_TAG%
                                        docker push %ECR_URI%:latest
                                        echo Successfully pushed to Amazon ECR.
                                    )
                                ) else (
                                    echo AWS CLI not found on PATH; proceeding with Docker Hub.
                                )
                            """
                        }
                    } catch (Exception ecrErr) {
                        echo "ECR Push note: ${ecrErr.message}. Proceeding with Docker Hub."
                    }

                    // 2. Push to Docker Hub
                    try {
                        echo "Pushing image to Docker Hub repository..."
                        if (isUnix()) {
                            sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                            sh "docker push ${IMAGE_NAME}:latest"
                        } else {
                            bat "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                            bat "docker push ${IMAGE_NAME}:latest"
                        }
                    } catch (Exception dhErr) {
                        echo "Docker Hub push notification: ${dhErr.message}"
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
                            docker stack deploy --with-registry-auth -c docker-stack.yml ${STACK_NAME}
                            docker stack services ${STACK_NAME}
                        """
                    } else {
                        bat """
                            docker stack deploy --with-registry-auth -c docker-stack.yml ${STACK_NAME}
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
