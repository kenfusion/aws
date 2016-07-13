#!/bin/env python2.7
import boto3
import sys

ec2 = boto3.resource('ec2')


def availableIp():
  allocationId = None

  allocatedIP_list = list(ec2.vpc_addresses.all())

  if len(allocatedIP_list) == 0:
    responseIp = ec2.meta.client.allocate_address(Domain='vpc')
    allocationId = responseIp['AllocationId']
  else:    
    for address in allocatedIP_list:
      if address.association_id:
        print "{0} is associated".format(address.public_ip)
        continue
      else:
        print "{0} is free".format(address.public_ip)
        return address.allocation_id

              
  if allocationId == None:
    try:
      responseIp = ec2.meta.client.allocate_address()
      newAddress = ec2.VpcAddress(responseIp['AllocationId'])
      print "{0} has just been allocated".format(newAddress.public_ip)
      return newAddress.allocation_id
    except boto3.exceptions.botocore.client.ClientError as e:
      print e
  
  return allocationId

print availableIp()