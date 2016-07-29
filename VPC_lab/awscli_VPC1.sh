#!/bin/bash

aws cloudformation create-stack --stack-name VPC1 --template-body file://./VPC1.json
