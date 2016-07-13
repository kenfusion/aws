#!/bin/env python2.7

import boto3
import sys


ec2 = boto3.resource('ec2')

# allocate eIP
try:
  responseAddress = ec2.meta.client.allocate_address()
except boto3.exceptions.botocore.client.ClientError as e:
  # TODO find easy wat to discover allocated eIP that is not assigned
  sys.exit(e)

subnetId_list = []
instanceId_list = []

# declare tags
vpc_tag_list = [{'Key':'Name', 'Value': 'myVPC'}]
igw_tag_list = [{'Key':'Name', 'Value': 'myIGW'}]
subnetA_tag_list = [{'Key':'Name', 'Value':'Private Subnet'}]
subnetB_tag_list = [{'Key':'Name', 'Value':'Public Subnet'}]
routePublic_tag_list = [{'Key':'Name', 'Value':'Public Route'}]
routePrivate_tag_list = [{'Key':'Name', 'Value':'Private Route'}]
privSG_tag_list = [{'Key':'Name', 'Value':'Private SG'}]
pubSG_tag_list = [{'Key':'Name', 'Value':'Public SG'}]
pubInstance_tag_list= [{'Key':'Name', 'Value':'Public Instance'}]
privInstance_tag_list= [{'Key':'Name', 'Value':'Private Instance'}]

#create  waiters
vpcWaiter = ec2.meta.client.get_waiter('vpc_available')
subnetWaiter = ec2.meta.client.get_waiter('subnet_available')
natWaiter = ec2.meta.client.get_waiter('nat_gateway_available')
instance_waiter = ec2.meta.client.get_waiter('instance_running')

#declare  cidr blocks
vpcCidrBlock = '10.0.0.0/16'
subnetAcidrBlock = '10.0.0.0/24'
subnetBcidrBlock = '10.0.1.0/24'
defaultRouteCiderBlock = '0.0.0.0/0'

#create VPC
myVPC = ec2.create_vpc(CidrBlock = vpcCidrBlock)

#create IGW
myIGW = ec2.create_internet_gateway()

#wait on VPC to be available
vpcWaiter.wait(VpcIds=[myVPC.id])

print '{} created'.format(myVPC.id)

# enable DNS hostnames
myVPC.modify_attribute(EnableDnsHostnames={'Value': True})

# attach IGW to VPC
myIGW.attach_to_vpc(VpcId=myVPC.id)

# create  subnets
subnetA = myVPC.create_subnet(CidrBlock = subnetAcidrBlock)
subnetId_list.append(subnetA.id)
subnetB = myVPC.create_subnet(CidrBlock = subnetBcidrBlock)
subnetId_list.append(subnetB.id)

# wait on subnets to be available
subnetWaiter.wait(SubnetIds=subnetId_list)

print '{} created'.format(subnetA.id)
print '{} created'.format(subnetB.id)

# Modify subnet to allocate to instances when they launch
ec2.meta.client.modify_subnet_attribute(
                                        SubnetId=subnetB.id,
                                        MapPublicIpOnLaunch={'Value': True}
                                        )
# create NAT

responseNat = ec2.meta.client.create_nat_gateway(
                                                 SubnetId=subnetB.id,
                                                 AllocationId = responseAddress['AllocationId']
                                                 )

natGatewayId = responseNat['NatGateway']['NatGatewayId']

# wait on NAT to be available
natWaiter.wait(NatGatewayIds = [natGatewayId])

print "{} created".format(natGatewayId)

# add route to NAT on main route table
mainRT = list(myVPC.route_tables.all())[0]
mainRT.create_route(
                    DestinationCidrBlock = defaultRouteCiderBlock,
                    NatGatewayId = natGatewayId
                    )

# create custom route table
myRouteTable = myVPC.create_route_table()

# add route to IGW on custom table
myRouteTable.create_route(
                          DestinationCidrBlock = defaultRouteCiderBlock,
                          GatewayId = myIGW.id
                          )

# associate custom route to public subnet
myRouteTable.associate_with_subnet(SubnetId = subnetB.id)

# create SGs

privSG = myVPC.create_security_group(
                                     GroupName='PrivSG',
                                     Description = "Security Group for Private Subnet"
                                     )
pubSG = myVPC.create_security_group(
                                    GroupName='PubSG',
                                    Description = "Security Group for Public Subnet"
                                    )

pubSG.authorize_ingress(
                        IpProtocol="tcp",
                        CidrIp="0.0.0.0/0",
                        FromPort=80,
                        ToPort=80
                        )
pubSG.authorize_ingress(
                        IpProtocol="tcp",
                        CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)

ipPermissions=[
               {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'UserIdGroupPairs': [
                                     {
                                     'GroupId': pubSG.id,
                                     'VpcId': pubSG.vpc_id
                                     }]}]

pubSG.authorize_ingress(
                        GroupId = privSG.group_id,
                        IpPermissions= ipPermissions
                        )

#TODO tighten egress rules

# launch instances
                                    
pubInstances = subnetB.create_instances(
                                        ImageId = 'ami-08111162',
                                        MinCount = 1,
                                        MaxCount = 1,
                                        InstanceType = 't2.nano',
                                        KeyName = 'mykey',
                                        SecurityGroupIds = [ pubSG.id ],
                                        ) 
for i in pubInstances:
    instanceId_list.append(i.id)

privInstances = subnetB.create_instances(
                                        ImageId = 'ami-08111162',
                                        MinCount = 1,
                                        MaxCount = 1,
                                        InstanceType = 't2.nano',
                                        KeyName = 'mykey',
                                        SecurityGroupIds = [ privSG.id ],
                                        ) 
for i in privInstances:
    instanceId_list.append(i.id)
    
instance_waiter.wait(InstanceIds = instanceId_list)

for i in instanceId_list:
  print 'instance {} created'.format(i)


                                    
# tag all the things!
myVPC.create_tags(Tags=vpc_tag_list)
myIGW.create_tags(Tags=igw_tag_list)
subnetA.create_tags(Tags=subnetA_tag_list)
subnetB.create_tags(Tags=subnetB_tag_list)
mainRT.create_tags(Tags=routePrivate_tag_list)
myRouteTable.create_tags(Tags=routePublic_tag_list)
pubSG.create_tags(Tags=pubSG_tag_list)
privSG.create_tags(Tags=privSG_tag_list)
for i in pubInstances:
    i.create_tags(Tags=pubInstance_tag_list)
for i in privInstances:
    i.create_tags(Tags=privInstance_tag_list)

print myVPC.id, myVPC.cidr_block

for subnet in myVPC.subnets.all():
  print subnet.id, subnet.availability_zone, subnet.available_ip_address_count, subnet.cidr_block, subnet.tags[0]['Value']
