ec2-tools is a set of tools with user friendly interface to assist ops dealing with Amazon ec2.

# Goals

* List ec2 instance in a user friendly style
* Show specific instance detail

# Usage

Install boto

 pip install boto

Add a configuration file: `config.py` with the aws access key and secret.

 AWS_ACCESS_KEY_ID = 'YOUR ACCESS KEY ID'
 AWS_SECRET_ACCESS_KEY = 'YOUR SECRET KEY'
 
List all the instance:
 python list_instance.py

Add a allow ip with ssh access to all the security group:
 python add_security_group.py 12.23.43.5/32
