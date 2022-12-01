# NOTICE
This project is for learning purposes 

# Prerequisites
I will assume that the avarage user know the basics
In order to replicate this project the following tools are needed:
* Docker
* Jenkins
* Helm
* yq
The above need to be on the same machine
* Kubernetes
* ArgoCD
The above need to be on the same machine
* Github account
* Dockerhub account
* AWS account

# Running steps:
* Changes made to the dev branch will trigger the Jenkins pipeline
* The pipeline will try to build the image with the updates
* On a successfull build, an update to the helm chart will occur
* The pipeline will push the updated Docker image to the Dockerhub
* The pipeline will merge the changes with the main/master branch
* The pipeline will push the changes to the HelmRepo on which the ArgoCD is monitoring
* Upon update to the HelmRepo repository, ArgoCD will update your Kubernetes environment

# Steps to copy this project:

* Installation of the tools
* Clone the JB_DEVOPS_Final to a clean repository on your Github account
* Create another branch apart from you main/master
* Clone the HelmRepo to a DIFFERENT, clean repository on your Github account
* Create an access tokens to both your Git and Docker accounts
* Import the JB_DEVOPS_Final Jenkinsfile to the Jenkins on your machine
* Update the parameters credentials and the references according to your account
* Import the ArgoCD Exports to your ArgoCD
* Update the ArgoCD tokens, references to your repository
* In the Dockerfile code update the reffenrences to your AWS account with your own accessID and secret

# Project purpose
The project will scan your AWS EC2 and print a report of the machines that are running with the following tags:
--filters "Name=tag:k8s.io/role/master,Values=1"  "Name=instance-state-code,Values=16”
you can change the tags in the Code/run_app.py

# Known problems
* Pushing changes failing on the git side
