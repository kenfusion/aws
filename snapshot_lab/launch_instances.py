#!/bin/env python2.7

import boto3

volume_id_list = []
instance_id_list = []
attach_dict = {}
volume_tag_list = [{'Key':'LamdaSnap', 'Value': 'True'}]
device = '/dev/xvdf'

ec2 = boto3.resource('ec2')
instance_waiter = ec2.meta.client.get_waiter('instance_running')
volume_waiter = ec2.meta.client.get_waiter('volume_available')
attach_waiter = ec2.meta.client.get_waiter('volume_in_use')

my_instances = ec2.create_instances(
                                    ImageId = 'ami-08111162',
                                    MinCount = 1,
                                    MaxCount = 3,
                                    InstanceType = 't2.nano',
                                    KeyName = 'mykey'
                                    )

for i in my_instances:
  instance_id_list.append(i.id)

for i in my_instances:
  v = ec2.create_volume(
                        Size=1,
                        AvailabilityZone='us-east-1a'
                        )
  attach_dict[v.id] = i.id
  volume_id_list.append(v.id)

instance_waiter.wait(InstanceIds=instance_id_list)

volume_waiter.wait(VolumeIds=volume_id_list)

for v in attach_dict:
  vol = ec2.Volume(v)
  vol.attach_to_instance(
                         InstanceId=attach_dict[v],
                         Device=device
                         )
attach_waiter.wait(VolumeIds=volume_id_list)

ec2.meta.client.create_tags(Resources=volume_id_list, Tags=volume_tag_list)
