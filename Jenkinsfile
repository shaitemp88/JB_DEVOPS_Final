//properties([pipelineTriggers([githubPush()])])

pipeline {
    // Agent config
    agent any
    // Environmant variables
    parameters {
		string(name: 'INTERVAL', defaultValue: "300", description: 'The time in seconds where the script run')
		string(name: 'GITPROJECT', defaultValue: "https://github.com/shaitemp88/JB_DEVOPS_Final", description: 'Git project code')
		string(name: 'GITBRANCH', defaultValue: "dev", description: 'Git branch')
	}
	environment {
	    INTERVAL = "${env.INTERVAL}"
	    GITPROJECT = "${env.GITPROJECT}"
	    GITBRANCH = "${env.GITBRANCH}"
	    DOCKERBUILD = "sbitton/jb_devops_final:v-${env.BUILD_NUMBER}"
        HELMBUILD = "shaitemp88/HelmRepo"
	    DOCKERRUNNAME = "run1"
	    AUTHDOCERU = "sbitton"
	    AUTHDOCERP = "dckr_pat_4sJ6C5h2pJJ3_z55Ki5H_SvknFs"
	}
    stages {
        stage ('Init') {
            steps {
                cleanWs()
                // We need to explicitly checkout from SCM here
                echo "Building ${env.JOB_NAME}..."
                echo "Interval $INTERVAL..."
                // sh 'docker rm ${docker ps --all -q}'
                // sh 'docker image rm ${docker images -q}'
                // sh 'printenv'
            }
        }
        stage ('Get code') {
            //agent {docker {image ciConfig.buildImage}}
            steps {
                script {
                    // consul
                    //sh 'git clone -b main https://github.com/shaitemp88/Development.git'
                    sh 'git clone -b dev https://github.com/shaitemp88/JB_DEVOPS_Final'
                    //git branch: '$GITBRANCH', url: 'https://$GITPROJECT'
                }
            }
        }
        stage ('Build Dockerfile'){
            steps{
                script {
                    sh 'ls'
                    sh 'docker build -t $DOCKERBUILD ./JB_DEVOPS_Final/'
                }
            }
        }
        stage ('Merge dev with branch'){
            steps {
                script {
                    echo "TODO: Merge dev with branch"
                }
            }
        }
        stage ('Commit changes to HelmRepo'){
            steps {
                script {
                    echo "TODO: Commit changes to HelmRepo"
                }
            }
        }
        stage('Update helm values file') {
            steps {
                script {
                    sh """
                        cd ./JB_DEVOPS_Final/mychart
                        cat values.yaml | yq eval -i '.image.tag = $BUILD_NUMBER' values.yaml
                        cat values.yaml | yq eval -i '.image.repository = "$DOCKERBUILD"' values.yaml
                        yq eval -e values.yaml
                        cd ../..
                    """
                }
            }
        }
        stage('Create helm package'){
            steps{
                script {
                    sh 'pwd'
                    sh 'ls'
                    sh 'cd JB_DEVOPS_Final'
                    sh 'ls'
                    sh 'cd ..'
                    sh 'mkdir HelmRepo'
                    sh 'cd HelmRepo'
                    sh 'helm package ../JB_DEVOPS_Final/mychart/'
                    sh 'cd ..'
                }
            }
        }
        stage ('Upload Docker image'){
            steps{
                script{
                    sh 'docker login -u $AUTHDOCERU -p $AUTHDOCERP'
                    sh 'docker push $DOCKERBUILD'
                }
            }
        }
        stage('Remove old Docker containers'){
            steps{
                script{
                    def doc_containers = sh(returnStdout: true, script: 'docker container ps -aq').replaceAll("\n", " ") 
                    if (doc_containers) {
                        sh "docker stop ${doc_containers}"
                        sh "docker rm -f ${doc_containers}"
                    }
                }
            }
        }
        /*stage ('Run Docker from build')
        {
            steps{
                script {
                    // SUCCESS_BUILD=`wget -qO- http://jenkins_url:8080/job/jobname/lastSuccessfulBuild/buildNumber`
                    sh 'docker run --env INTERVAL=$INTERVAL --name $DOCKERRUNNAME -tid $DOCKERBUILD'
                    sh 'sleep 10'
                    sh 'docker logs $DOCKERRUNNAME'
                }
            }
        }*/
    }
}
