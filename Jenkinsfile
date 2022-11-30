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
        AUTHGITU = "shaitemp88"
        AUTHGITP = "12WE\$%rt"
	}
    stages {
        stage ('Init') {
            steps {
                cleanWs()
                // We need to explicitly checkout from SCM here
                echo "Building ${env.JOB_NAME}"
                echo "Interval $INTERVAL"
                echo "Git project $GITPROJECT"
            }
        }
        stage ('Get code') {
            //agent {docker {image ciConfig.buildImage}}
            steps {
                script {
                    sh 'git clone -b $GITBRANCH https://$GITPROJECT'
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
                    sh """
                        git remote add origin https://$AUTHGITU:$AUTHGITP@github.com/UserName/yourRepo.git
                        git checkout main
                        git merge origin/$GITBRANCH
                    """
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
                    sh """
                        mkdir HelmRepo
                        cd ./HelmRepo
                        helm package ../JB_DEVOPS_Final/mychart/
                        cd ..
                    """
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
