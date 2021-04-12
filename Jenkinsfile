pipeline {
    agent none
    options { skipDefaultCheckout(false) }
    stages {
        stage('Docker build') {
            agent any
            steps {
				script{
					mattermostSend (
									color: "#2A42EE", 
									message: "빌드 시작: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Link to build>)"
					)
				}
				sh 'docker build -t base-pjt-back:latest ./exec/back'
				sh 'docker build -t base-pjt-front:latest ./exec/front/jjal'
            }
        }
        stage('Docker Container rm') {
	        agent any
	        steps {
				script {
					sh 'docker ps -f name=base-pjt-back -q | xargs --no-run-if-empty docker container stop'
					sh 'docker container ls -a -fname=base-pjt-back -q | xargs -r docker container rm'
					sh 'docker ps -f name=base-pjt-front -q | xargs --no-run-if-empty docker container stop'
					sh 'docker container ls -a -fname=base-pjt-front -q | xargs -r docker container rm'
					sh 'docker ps -a -f "status=exited" -q | xargs -r docker container rm'
					sh 'docker rmi $(docker images -f "dangling=true" -q)'
				}
	        }
	    }
        stage('Docker run') {
            agent any
            steps {
		        sh 'docker run -it -d -p 8000:8000 -v /content:/content --name base-pjt-back --network base-pjt-network base-pjt-back:latest'
		        sh 'docker run -it -d -p 80:80 -p 443:443 -v /volumes/keys:/usr/keys --name base-pjt-front --network base-pjt-network base-pjt-front:latest'
            }
        }
    }
	post {
        success {
			script{
				mattermostSend (
					color: "good", 
					message: "빌드 성공: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Link to build>)"
				)
			}
        }
        failure {
			script{
				mattermostSend (
					color: "danger", 
					message: "빌드 실패: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Link to build>)"
				)
			}
        }
	}
}
