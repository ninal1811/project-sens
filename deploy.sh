#!/bin/bash
# This shell script deploys a new version to a server.

PROJ_DIR=project-sens
VENV=venv
PA_DOMAIN="projectsens.pythonanywhere.com"
PA_USER='projectsens'
PA_API_TOKEN=2c7f9c0897f957596cba6c4ad8b31ab0542ce914 
echo "Project dir = $PROJ_DIR"
echo "PA domain = $PA_DOMAIN"
echo "Virtual env = $VENV"

if [ -z "$PROJECTSENS_PA_PWD" ]
then
    echo "The PythonAnywhere password var (PROJECTSENS_PA_PWD) must be set in the env."
    exit 1
fi

echo "PA user = $PA_USER"
echo "PA password = $PROJECTSENS_PA_PWD"

echo "SSHing to PythonAnywhere."
sshpass -p $PROJECTSENS_PA_PWD ssh -o "StrictHostKeyChecking no" $PA_USER@ssh.pythonanywhere.com << EOF
    cd ~/$PROJ_DIR; PA_USER=$PA_USER PROJ_DIR=~/$PROJ_DIR VENV=$VENV PA_DOMAIN=$PA_DOMAIN ./rebuild.sh
EOF
