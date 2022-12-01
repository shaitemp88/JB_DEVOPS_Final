pipeline {
    // Agent config
    agent any
    // Environmant variables
    parameters {
		string(name: 'INTERVAL', defaultValue: "300", description: 'The time in seconds where the script run')
		string(name: 'GITPROJECT', defaultValue: "github.com/shaitemp88/JB_DEVOPS_Final", description: 'Git project code')
        string(name: 'HELMPROJECT', defaultValue: "github.com/shaitemp88/HelmRepo", description: 'Git project code')
		string(name: 'GITBRANCH', defaultValue: "dev", description: 'Git branch')
	}
	environment {
	    INTERVAL = "${env.INTERVAL}"
	    GITPROJECT = "${env.GITPROJECT}"
	    GITBRANCH = "${env.GITBRANCH}"
        HELMPROJECT = "${env.HELMPROJECT}"
        GITMAINBRANCH = "main"
	    DOCKERBUILD = "sbitton/jb_devops_final:v-${env.BUILD_NUMBER}"
	    DOCKERRUNNAME = "run1"
	    AUTHDOCERU = "sbitton"
	    AUTHDOCERP = "dckr_pat_4sJ6C5h2pJJ3_z55Ki5H_SvknFs"
        GITACCESSTOKEN = "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"
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
            steps {
                script {
                    sh 'git clone -b $GITBRANCH https://$GITPROJECT'
                }
            }
        }
        stage ('Build Dockerfile'){
            steps{
                script {
                    sh 'docker build -t $DOCKERBUILD ./JB_DEVOPS_Final/'
                }
            }
        }
        stage ('Merge dev with branch'){
            steps {
                script {
                    sh 'git init'
                    sh 'git remote add origin https://$GITACCESSTOKEN@$GITPROJECT'
                    sh 'git fetch'
                    sh 'git checkout $GITBRANCH'
                    sh 'git fetch'
                    sh 'git checkout $GITMAINBRANCH'
                    sh 'git fetch'
                    sh 'git merge $GITBRANCH --commit'
                    //sh 'git push origin $GITMAINBRANCH'
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
        stage ('Commit changes to HelmRepo'){
            steps {
                script {
                    sh """
                        git clone https://$HELMPROJECT
                        cd ./HelmRepo/mychart/
                        cp ../../JB_DEVOPS_Final/mychart/values.yaml values.yaml
                        cat values.yaml
                        git remote add helm https://$GITACCESSTOKEN@$HELMPROJECT
                        git add --all
                        git commit -m "update $DOCKERBUILD"
                    """
                    // sh 'git push helm $GITMAINBRANCH'
                }
            }
        }
        stage('Create helm package'){
            steps{
                script {
                    sh """
                        cd ./HelmRepo/mychart/
                        ls
                        helm package .
                        cd ../..
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
