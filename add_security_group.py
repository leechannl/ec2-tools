#! /usr/bin/env python
"""Add ip to EC2 security group. Right now only support port 22.
    :input: ip and netmask. e.g. 10.24.45.35/32
    """

import sys

from boto.ec2.connection import EC2Connection
from boto.exception import EC2ResponseError
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

conn = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

security_groups = conn.get_all_security_groups()

ip = sys.argv[1]

if __name__ == '__main__':
    print ip
    for sg in security_groups:
        try:
            sg.authorize(ip_protocol='tcp', from_port=22, to_port=22,
                cidr_ip=ip)
            print "Add rule to %s " % sg.name
        except EC2ResponseError as e:
            print 'Rules already exist.'
