#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Module: sensors
#
# Author: Michael L. Martin (mmartin4242@gmail.com)

import sensors

descriptors = list()

def coretemp_handler(name):
    
    sensors.init()
    value = 0
    try:
        for chip in sensors.iter_detected_chips():
            if chip.prefix.startswith('coretemp'):
                for feature in chip:
                    if feature.label == name:
                        value = feature.get_value()
                        break
    except:
        print "WTF?!?"
    finally:
        sensors.cleanup()
    return value

def metric_init(params):
    global descriptors
    
    metric_group = params.get('metric_group', 'coretemp')
    sensors.init()

    for chip in sensors.iter_detected_chips():
        for feature in chip:
            if chip.prefix.startswith('coretemp'):
                descriptors.append({
                    'name': feature.label,
                    'call_back' : coretemp_handler,
                    'time_max' : 60,
                    'units': 'C',
                    'format' : '%.2f',
                    'slope' : 'both',
                    'description' : 'CPU Core Temperature',
                    'groups' : metric_group,
                }) 
    sensors.cleanup()

    return descriptors

def metric_cleanup():
    pass

#This code is for debugging and unit testing
if __name__ == '__main__':
    metric_init({})
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for %s is %u' % (d['name'],  v)
        print 'Descriptor: %s' % d
