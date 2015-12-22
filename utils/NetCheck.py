# -*- coding: cp936 -*-
import os,io

def ping_ipaddress(ip):
    '''Check the network'''
    ping_cmd = '%s %s' %('ping', ip)
    r = os.popen(ping_cmd)
    response = r.readlines()
    print response,
    for line in response:
        if 'TTL' in line:
            print 'ping ok'
            return True
    print 'ping fail'
    return False


# ping_ipaddress('127.0.0.1')
