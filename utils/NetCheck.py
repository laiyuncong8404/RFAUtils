# -*- coding: cp936 -*-
import io
import os


def ping_ipaddress(ip):
    '''Check the network'''
    ping_cmd = '%s %s' %('ping -n 1',ip)
    rr=os.popen(ping_cmd)
    rrr=rr.readlines()
    for line in rrr:
        if 'TTL' in line:
            print 'ping ok'
            return True
    print 'ping fail'
    return False

ping_ipaddress('127.0.0.1')
