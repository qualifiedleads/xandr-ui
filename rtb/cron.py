#!/bin/python
import datetime

import common.report as reports

# stub for future api pooling
def hourly_task():
    print ('NexiusApp API pooling...')
    reports.get_network_analytics()
	
if __name__=='__main__':hourly_task()
