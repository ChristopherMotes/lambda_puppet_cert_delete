import boto3
import paramiko
def worker_handler(event, context):

    s3_client = boto3.client('s3')
    ec2_client = boto3.client('ec2')
    #Download private key file from secure S3 bucket
    s3_client.download_file('motes-keys','keypair-311.pem', '/tmp/keyname.pem')

    keyfile = paramiko.RSAKey.from_private_key_file("/tmp/keyname.pem")
    sshcommand = paramiko.SSHClient()
    sshcommand.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # get puppetmaster instance IP
    masterDICT=ec2_client.describe_instances(
        Filters=[{'Name':'tag:Name','Values':['puppetamster']}]
    ) 

    #for reservations in masterDICT['Reservations']:
    #    for inst in reservations['Instances']:
    #        masterIP=inst['PrivateIpAddress']
    masterIP="192.168.0.50"
    # get client name
    instID=event['id']
    print "Connecting to " + masterIP
    sshcommand.connect( hostname = masterIP, username = "ec2-user", pkey = keyfile )
    print "Connected to " + masterIP
    command = "sudo curl -sX GET 'https://puppetdb.maint.motes:8081/pdb/query/v4/fact-contents'  --tlsv1   --cacert /etc/puppetlabs/puppet/ssl/certs/ca.pem   --cert /etc/puppetlabs/puppet/ssl/certs/`uname -n`.pem   --key /etc/puppetlabs/puppet/ssl/private_keys/`uname -n`.pem --data-urlencode 'query=[\"=\", \"value\", \"" + instID  + "\"]]' | awk -F '\"|:' ' { print $5 } '"
    print "Executing {}".format(command)
    stdin , stdout, stderr = sshcommand.exec_command(command)
    instName=stdout.read()

    command = "sudo docker exec puppetmaster /opt/puppetlabs/bin/puppet node clean " + instName
    print "Executing {}".format(command)
    stdin , stdout, stderr = sshcommand.exec_command(command)
    print stdout.read()
    print stderr.read()

    return
    {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }

