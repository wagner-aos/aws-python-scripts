#!/bin/bash

# --------------------------------------------------------- #
# AWS_SESSION_TOKEN 1.0.0                                   #
# Script para criação das variaveis de ambiente AWS         #
# via profile.                                              #
#                                                           #
# Depende do modulo NPM: aws-assume !!!                     #
# Instalação: npm install aws-assume -g                     #
#                                                           #  
# usage: . aws-session-token.sh <profile>                   #
#                                                           # 
# Author: Wagner Alves                                      # 
#   Date: 2018-04-02                                        # 
#                                                           # 
# --------------------------------------------------------- #

clear

if [ $# -eq 0 ]; then
   echo "Por favor digite o profile!"   
elif [ -z $1 ]; then
   echo "Digite . aws-session-token.sh <dev, hml, ppd, prod>;"
else

	echo "Setting env variables to profile: "$1

	# unsetting aws env variables.
	unset AWS_SESSION_TOKEN 
	unset AWS_SECRET_ACCESS_KEY
	unset AWS_ACCESS_KEY_ID

	# exec aws-assume npm module.
	AWS_TOKENS="$(aws-assume $1)"

	# spliting result
	LIST_ENVS=$(echo $AWS_TOKENS | tr "''" "\n")

	# export AWS_SESSION_TOKEN, AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID.
	for VARIABLE in $LIST_ENVS
	do
	    export $VARIABLE
	done

	export AWS_REGION=us-east-1
	export ENVIRONMENT=$1

	# verifying variables.
	env | grep AWS
	env | grep ENVIRONMENT
	
fi
