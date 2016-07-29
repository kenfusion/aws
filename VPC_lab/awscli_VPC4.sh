#!/bin/bash

aws cloudformation create-stack --stack-name VPC4 --template-body file://./VPC4.json\
                                --parameters ParameterKey=KeyName,ParameterValue=mykey\
                                             ParameterKey=AvailabilityZone,ParameterValue=us-east-1a\
                                --capabilities CAPABILITY_IAM
