#!/usr/bin/env python

import sys
import os
import subprocess
import time
from pprint import pprint
from zapv2 import ZAPv2

try:
# Start ZaProxy as Daemon as it is required to run all of this script
    print 'Starting ZAP ...'
    subprocess.Popen(['zap.sh','-daemon','-config api.disablekey=true'],stdout=open(os.devnull,'w'))
    print 'Waiting for ZAP to load, 10 seconds ...'
    time.sleep(10)

    apikey = ''
    zap = ZAPv2(apikey=apikey)

    # Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090

    #zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})


    def spiderScan(targetScan):
        # do stuff
        print 'Accessing target %s' % target

        # try have a unique enough session...

        zap.urlopen(target)

        # Give the sites tree a chance to get updated

        time.sleep(2)

        print 'Spidering target %s' % target

        scanid = zap.spider.scan(target)

        # Give the Spider a chance to start

        time.sleep(2)

        while (int(zap.spider.status(scanid)) < 100):
            print 'Spider progress %: ' + zap.spider.status(scanid)
            time.sleep(2)

        print 'Spider completed'
        # Give the passive scanner a chance to finish
        time.sleep(5)

        print 'Scanning target %s' % target
        scanid = zap.ascan.scan(target)
        while (int(zap.ascan.status(scanid)) < 100):
            print 'Scan progress %: ' + zap.ascan.status(scanid)
            time.sleep(5)

        print 'Scan completed'

        # Report the results

        print 'Hosts: ' + ', '.join(zap.core.hosts)
        print 'Alerts: '
        pprint (zap.core.alerts())

        return

    target = 'http://www.traklife.com/radio/'
    targetScan = target

    spiderScan(targetScan)


    pprint(world.zap.core.alerts())
    report_type = 'xml'
    report_file = 'sample_report.xml'
    with open(report_file, 'a') as f:
        xml = world.zap.core.xmlreport()
        f.write(xml)
        print('Success: {1} report saved to {0}'.format(report_file, report_type.upper()))
    world.zap.core.shutdown()

except KeyboardInterrupt:
    print 'Interrupted'
    sys.exit(0)
    world.zap.core.shutdown()
# random-projects
