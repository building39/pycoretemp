#!/usr/bin/env python
import sensors
CORETEMP = 'coretemp'
descriptors = []

def temp_handler(name): 
    sensors.init()
    temp = 0.0
    try:
        for chip in sensors.iter_detected_chips():
            if chip.prefix == CORETEMP:
                for feature in chip:
                    if '%s Temperature' % feature.label == name:
                        temp = feature.get_value()
    finally:
        sensors.cleanup()
    return temp

def metric_init(params):
    global descriptors
    
    sensors.init()
    corelist = []
    
    try:
        for chip in sensors.iter_detected_chips():
            if chip.prefix == CORETEMP:
                for feature in chip:
                    if feature.label.startswith('Core'):
                        corelist.append("%s Temperature" % feature.label)
    except:
        raise
    finally:
        sensors.cleanup()

    for core in corelist:
        print 'name: %s' % core
        descriptors.append({'name': core,
                                'call_back': temp_handler,
                                'time_max': 90,
                                'value_type': 'float',
                                'units': 'Celsius',
                                'slope': 'both',
                                'format': '%.2f',
                                'description': 'Temperature of %s' % core,
                                'groups': 'Node Health'})
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
