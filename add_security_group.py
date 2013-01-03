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


def add_ssh(ip, security_groups):
    """Allow ssh access to all the security group from this ip."""
    for sg in security_groups:
        try:
            sg.authorize(ip_protocol='tcp', from_port=22, to_port=22,
                cidr_ip=ip)
            print "Allow ssh from %s " % ip
        except EC2ResponseError as e:
            print 'Rules already exist.'


def add_chef(ip, security_groups):
    """Allow chef web UI and web API access from this ip."""
    chef_sg = [sg for sg in security_groups if sg.name == 'chef-server']
    if len(chef_sg) > 1:
        print "You have duplicated security group name."
        sys.exit(1)
    sg = chef_sg[0]
    try:
        sg.authorize(ip_protocol='tcp', from_port=4000, to_port=4000,
                cidr_ip=ip)
        print "Allow Chef API port from %s" % ip
        sg.authorize(ip_protocol='tcp', from_port=4040, to_port=4040,
                cidr_ip=ip)
        print "Allow Chef web UI port from %s" % ip
    except EC2ResponseError as e:
        print 'Rules already exist.'


def add_zabbix(ip, security_groups):
    """Allow zabbix web UI access from this ip."""
    zabbix_sg = [sg for sg in security_groups if sg.name == 'zabbix']
    if len(zabbix_sg) > 1:
        print "You have duplicated security group name."
        sys.exit(1)
    sg = zabbix_sg[0]
    try:
        sg.authorize(ip_protocol='tcp', from_port=80, to_port=80,
                cidr_ip=ip)
        print "Allow zabbix web UI port from %s" % ip
    except EC2ResponseError as e:
        print 'Rules already exist.'


def add_hadoop(ip, security_groups):
    """Allow hadoop web UI access from this ip."""
    hadoop_sg = [sg for sg in security_groups if sg.name == 'zabbix']
    if len(hadoop_sg) > 1:
        print "You have duplicated security group name."
        sys.exit(1)
    sg = hadoop_sg[0]
    try:
        sg.authorize(ip_protocol='tcp', from_port=50030, to_port=50030,
                cidr_ip=ip)
        sg.authorize(ip_protocol='tcp', from_port=50070, to_port=50070,
                cidr_ip=ip)
        sg.authorize(ip_protocol='tcp', from_port=60030, to_port=60030,
                cidr_ip=ip)
        print "Allow hadoop web UI port from %s" % ip
    except EC2ResponseError as e:
        print 'Rules already exist.'


if __name__ == '__main__':
    add_ssh(ip, security_groups)
    add_chef(ip, security_groups)
    add_zabbix(ip, security_groups)
    add_hadoop(ip, security_groups)
