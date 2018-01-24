#!/usr/bin/env python

import sys
import os
import subprocess
import time
from pprint import pprint
from zapv2 import ZAPv2

# Active Scan Module

def activeScan(targetScan):
    # do stuff
    print 'Starting Active Scan'

    print 'Scanning target %s' % target[i]

    scanid = zap.ascan.scan(target[i])

    #Show Active Scan Progress
    while (int(zap.ascan.status(scanid)) < 100):
        print 'Scan progress %: ' + zap.ascan.status(scanid)

        # Give enough time for Active Scan to finish

        time.sleep(5)

    print 'Scan completed'

    return

# Spider Scan module
def spiderScan(targetScan):
    # do stuff
    print 'Accessing target %s' % target[i]

    # try have a unique enough session...

    print 'Spidering target %s' % target[i]

    scanid = zap.spider.scan(target[i])

    # Give the Spider a chance to start

    time.sleep(2)

    while (int(zap.spider.status(scanid)) < 100):
        print 'Spider progress %: ' + zap.spider.status(scanid)
        time.sleep(2)

    print 'Spider completed'
    # Give the passive scanner a chance to finish
    time.sleep(5)
    return

def showResults():
    #print ('Hosts: ' + ', '.join(zap.core.hosts))
    #print ('Sites: ' + ', '.join(zap.core.sites))
    #print ('Urls: ' + ', '.join(zap.core.urls))
    #print ('Alerts: ')

    #pprint (zap.core.alerts())


    # Writes the XML and HTML reports that will be exported to the workspace.

    fileName1 = time.strftime("%c")
    fileName2 = target[i].replace("http://","").replace("/",("-"))
    f = open('Target : '+fileName2+' Tanggal : '+fileName1+'.xml','w')
    f2 = open('Target : '+fileName2+' Tanggal : '+fileName1+'.html','w')
    f.write(zap.core.xmlreport(zap))
    f2.write(zap.core.htmlreport(zap))

    f.close()
    f2.close()

    print 'Result saved, file name : '+'Target : '+fileName2+' Tanggal : '+fileName1+'.html'

def mainZap():
    print 'Starting ZAP ...'
    subprocess.Popen(['zap.sh','-daemon'],stdout=open(os.devnull,'w'))
    print 'Waiting for ZAP to load, 20 seconds ...'
    #Give time ZAP to load
    time.sleep(20)



try:

   

    #Open Target File
    target = [line.rstrip('\n') for line in open('list.txt')]
    jumlahTarget = len(target)
    i = 0
    #targetScan = target


    

    while i<jumlahTarget:
	apikey = ''
    	zap = ZAPv2(apikey=apikey)

	mainZap()
        zap.urlopen(target[i])

        # Give the sites tree a chance to get updated

        time.sleep(2)

        spiderScan(target[i])
        activeScan(target[i])
        showResults()
        i+=1

        time.sleep(5)
	# Shutting down ZaProxy daemon
	zap.core.shutdown()

    
    


# Handle Keyboard Interrupt and Shuttting Down ZAP daemon
except KeyboardInterrupt:
    print 'Interrupted'
    sys.exit(0)
    zap.core.shutdown()
except NameError:
    print 'An Error has been detected...'
    print 'Shutting Down Program...'
    sys.exit(0)
    zap.core.shutdown
