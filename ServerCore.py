#!/usr/bin/env python

"""
Technic ServerCore v0.1
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
    if args.verbose: print sys.argv
    if args.listPacks:
	if len(sys.argv) > 2:
	    print "Error: Too many args"
            sys.exit(2)     
	else:
 	    listPacks()
    if args.pack: setPack()

def getPacks ():

    global availPacks, mirrorURL
    rawJSON = urllib2.urlopen('http://solder.technicpack.net/api/modpack').read()
    solderJSON = json.loads(rawJSON)
    mirrorURL = solderJSON['mirror_url']
    availPacks = solderJSON['modpacks']

def getPackInfo ():

    print

def setPack ():

    global currentPack
    print args.pack  

def listPacks ():

    print "\n\rModpacks:"
    print "==========="
    for key in availPacks:
        print '{0} ==> {1}'.format(availPacks[key], key)
    print
        

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser( epilog="Try 'ServerCore --help' for more information.")
        parser.add_argument ('-l', '--listPacks', action='store_true', default=False, help='list all available modpacks')
	parser.add_argument ('pack', nargs='?',  action='store', help='determines which pack to use')
	parser.add_argument ('--verbose', action='store_true', default=False, help='verbose output')
        parser.add_argument ('-v', '--version', action='version', version=globals()['__doc__'])
        args = parser.parse_args()
#        if not len(sys.argv) > 1:
#            parser.error ('missing argument')
        if args.verbose: print time.asctime()
	getPacks()
	main()
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
