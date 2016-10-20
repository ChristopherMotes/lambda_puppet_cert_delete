import boto3
import paramiko
def worker_handler(event, context):

    s3_client = boto3.client('s3')
    #Download private key file from secure S3 bucket
    s3_client.download_file('s3-key-bucket','keys/keypair-311.pem', '/tmp/keyname.pem')

    keyfile = paramiko.RSAKey.from_private_key_file("/tmp/keyname.pem")
    sshcommand = paramiko.SSHClient()
    sshcommand.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # get puppetmaster instance name
    

    host=event['IP']
    print "Connecting to " + host
    sshcommand.connect( hostname = host, username = "ec2-user", pkey = keyfile )
    print "Connected to " + host

    command = "sudo docker exec puppetmaster /opt/puppletlabs/bin/puppet node clean " + instName
    print "Executing {}".format(command)
    stdin , stdout, stderr = c.exec_command(command)
    print stdout.read()
    print stderr.read()

    return
    {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }

