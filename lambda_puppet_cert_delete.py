import boto3
import paramiko
def worker_handler(event, context):

    s3_client = boto3.client('s3')
    #Download private key file from secure S3 bucket
    s3_client.download_file('s3-key-bucket','keys/keypair-311.pem', '/tmp/keyname.pem')

    keyfile = paramiko.RSAKey.from_private_key_file("/tmp/keyname.pem")
    sshcommand = paramiko.SSHClient()
    sshcommand.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # get puppetmaster instance IP
    masterDICT=client.describe_instances(
        Filters=[{'Name':'tag:Name','Values':['puppetamster']}]
    ) 

    for reservations in masterDICT['Reservations']:
        for inst in reservations['Instances']:
        masterIP=inst['PrivateIpAddress']
    
    # get client name
    instID=event['id']
    clientnameDICT=client.describe_instances(
        InstanceIds = [instID]
    )
    for reservations in clientnameDICT['Reservations']:
        for inst in reservations['Instances']:
            print inst
            instName=inst['PrivateDnsName']

    print "Connecting to " + masterIP
    sshcommand.connect( hostname = host, username = "ec2-user", pkey = keyfile )
    print "Connected to " + masterIP

    command = "sudo docker exec puppetmaster /opt/puppletlabs/bin/puppet node clean " + instName
    print "Executing {}".format(command)
    stdin , stdout, stderr = sshcommand.exec_command(command)
    print stdout.read()
    print stderr.read()

    return
    {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }

