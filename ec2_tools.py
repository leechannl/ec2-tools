#! /usr/bin/env python

from boto.ec2.connection import EC2Connection


conn = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

reservations = conn.get_all_instances()

# get the instance list
instances = [res.instances[0] for res in reservations]

# get the instance detail dict list
dict_keys = ['id', 'name', 'group', 'ip', 'private_ip', 'flavor', 'image', 'ssh_key' 'status']
detail_info = [dict(zip(dict_keys, [x.id,x.tags['Name'],x.groups[0].name,x.ip_address,x.private_ip_address,x.instance_type,x.image_id,x.key_name,x.state])) for x in inst]

# pretty print the list in a colored table

