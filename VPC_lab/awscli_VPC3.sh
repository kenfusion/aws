#!/bin/bash

aws cloudformation create-stack --stack-name VPC3 --template-body file://./VPC3.json\
                                --parameters ParameterKey=KeyName,ParameterValue=mykey\
                                --capabilities CAPABILITY_IAM
