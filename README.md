## Create Lamda Zip file
```
pip install virtualenv
mkdir cert_del_env
virtualenv --python=/usr/bin/python2.7 cert_del_env
source cert_del_env/bin/activate
pip install pycrypto
sudo yum install libffi-devel
sudo yum install openssl-devel
pip install paramiko
cd lambda_puppet_cert_delete/
zip ../lambda_puppet_cert_delete.zip lambda_puppet_cert_delete.py 
cd cert_del_env/lib/python2.7/site-packages/
zip -r ~/lambda_puppet_cert_delete.zip *
cd ../../../lib64/python2.7/site-packages/
zip -r ~/lambda_puppet_cert_delete.zip *
```
```

