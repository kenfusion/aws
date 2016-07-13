import boto3

def lambda_handler(event, context):
  # create ec2 resource instance
  ec2 = boto3.resource('ec2')

  # gather list of instances
  print "Gathering list of instances..."
  instances = list(ec2.instances.all())

  # test if there are 0 instances
  if len(instances) == 0 :
    print "There are no instances."
  else:
    # print out the id and state of each instance
    print "{} instance(s) found:".format(len(instances))
    for instance in instances:
	    print "Instance ID: {0} Instance State: {1}".format(instance.id, instance.state['Name'])
