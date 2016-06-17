#!/bin/python
import datetime
import common.report as reports
import threading
import csv

def analize_csv(csvFile, modelClass, fieldNames):
    reader = csv.reader(csvFile)
    result=[]
    for row in csv:
        # if first: 
            # first=False
            # continue
        c=modelClass()
        for field, fName in zip(row,fieldNames):
            c.__dict__[fName]=field
        if c.hasattr('TransformFields'):
            c.TransformFields()
        result.append(c)
    return result

# Task, executed twice in hour. Get new data from NexusApp
def hourly_task():
    print ('NexusApp API pooling...')
    #reports.get_specifed_report('network_analytics')
    f=reports.get_specifed_report('site_domain_performance')
    r=analize_csv(f, SiteDomainPerformanceReport, reports.column_sets_for_reports['site_domain_performance'])
    print r[0]
    print r[1]
    
if __name__=='__main__':hourly_task()
