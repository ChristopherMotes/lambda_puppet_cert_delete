import boto3
def lambda_handler(event, context):
    instID = event['detail']['instance-id']
    instState = event['detail']['state']
    root_device_type = "Who cares"
    print "instance state is " + instState
    client = boto3.client('ec2')
    instDICT=client.describe_instances(
            InstanceIds = [instID]
        )
    if instState == 'stopped':
        for r in instDICT['Reservations']:
            for inst in r['Instances']:
                root_device_type=inst['RootDeviceType']
    
    if instState == 'terminated' or ( instState == 'stopped' and root_device_type == 'instance-store' ):
        print "Invoking Key Delete with instance ID " + instID
        client = boto3.client('lambda')
        invokeResponse=client.invoke(
            FunctionName='lambda_puppet_cert_delete',
            InvocationType='Event',
            LogType='Tail',
            Payload='{"id":"'+ instID +'"}'
        )
        print invokeResponse
    return{
        'message' : "Trigger function finished"
    }
