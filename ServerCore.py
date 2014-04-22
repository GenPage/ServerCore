#!/usr/bin/env python

"""
Technic ServerCore
By: GenPage
Copyright (c) 2013 Syndicate, LLC <http://www.technicpack.net/>
"""

import sys, os, traceback, argparse
import time
import re
import json
import urllib2
import pprint

def main ():

    global args
    # TODO: Do something more interesting here...
    print args

def getPacks ():

    global availPacks, mirrorURL
    rawJSON = urllib2.urlopen('http://solder.technicpack.net/api/modpack').read()
    solderJSON = json.loads(rawJSON)
    mirrorURL = solderJSON['mirror_url']
    availPacks = solderJSON['modpacks']

def getPackInfo ():

    global currentPack

def listPacks ():

    pprint.pprint(availPacks)
        

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser( usage=globals()['__doc__'])
        parser.add_argument ('-l', '--listPacks', action='store_true', default=False, help='list all available modpacks')
	parser.add_argument ('-s', '--setPack', action='store',  help='verbose output')
	parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_argument ('--version', action='version', version='%(prog)s 0.1')
        args = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if args.verbose: print time.asctime()
	getPacks()
	if args.listPacks: listPacks()
	else: main()
        if args.verbose: print time.asctime()
        if args.verbose: print 'TOTAL TIME IN MINUTES:',
        if args.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
