#!/usr/bin/env python
import socket
BLKSIZE = 4096
HOST = 'localhost'
PORT = 7634
descriptors = []

def temp_handler(name):
    #import pydevd; pydevd.settrace(host='hypercat')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    data = sock.recv(BLKSIZE)
    drives = data.split('||')
    temp = 0.0
    try:
        for entry in drives:
            if entry.startswith('|'):
                entry = entry[1:]
            if entry.endswith('|'):
                entry = entry[:-1]
            drive, dname, temp, unit = entry.split('|')
            if drive == 'Drive %s Temperature' % name:
                break
    except:
        pass
    finally:
        sock.close()
    return float(temp)

def metric_init(params):
    global descriptors
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    data = sock.recv(BLKSIZE)
    drives = data.split('||')
    drivelist = []
    for entry in drives:
        if entry.startswith('|'):
                entry = entry[1:]
        if entry.endswith('|'):
            entry = entry[:-1]
        drivelist.append(entry.split('|')[0])
    
    sock.close()

    for drive in drivelist:
        
        descriptors.append({'name': 'Drive %s Temperature' % drive.split('/')[-1],
                                'call_back': temp_handler,
                                'time_max': 90,
                                'value_type': 'float',
                                'units': 'Celsius',
                                'slope': 'both',
                                'format': '%.2f',
                                'description': 'Temperature of %s' % drive,
                                'groups': 'Drive Health'})
    return descriptors

def metric_cleanup():
    '''Clean up the metric module.'''
    pass

#This code is for debugging and unit testing
if __name__ == '__main__':
    metric_init({})
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for >%s< is %s' % (d['name'],  v)
