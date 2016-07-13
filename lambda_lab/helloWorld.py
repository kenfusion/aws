import json
from botocore.vendored import requests

def lambda_handler(event, context):
  SUCCESS = 'SUCCESS'
  FAILED = 'FAILED'
  request_recieved =  "REQUEST RECIEVED: {}".format(json.dumps(event))
  print request_recieved
  
  # respond to any Delete request with SUCCESS

  responseStatus = SUCCESS
  responseData = {}
  
  if event['RequestType'] == 'Delete':
    send(event, context, responseStatus, responseData)

  # respond to any other request with Success
  responseData['Response'] = 'Hello World!'
  send(event, context, responseStatus, responseData)

    
def send(event, context, responseStatus, responseData):
  responseUrl = event['ResponseURL']
  
  responseBody = {}
  responseBody['Status'] = responseStatus
  responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
  responseBody['PhysicalResourceId'] = context.log_stream_name
  responseBody['StackId'] = event['StackId']
  responseBody['RequestId'] = event['RequestId']
  responseBody['LogicalResourceId'] = event['LogicalResourceId']
  responseBody['Data'] = responseData
  
  json_responseBody = json.dumps(responseBody)
    
  headers = {
             'content-type' : '', 
             'content-length' : str(len(responseBody))
             }

  print 'RESPONSE URL: {}'.format(responseUrl)
  print 'HEADERS: {}'.format(headers)
  print 'RESPONSE BODY: {}'.format(json_responseBody)
   
  
  try:
    response = requests.put(
                            responseUrl,
                            data=json_responseBody,
                            headers=headers
                            )
    print "Status code: " + response.reason
  except Exception as e:
    print "send(..) failed executing requests.put(..): " + str(e)