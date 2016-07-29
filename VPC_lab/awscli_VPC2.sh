#!/bin/bash

aws cloudformation create-stack --stack-name VPC2 --template-body file://./VPC2.json
