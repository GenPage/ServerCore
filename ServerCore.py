#!/usr/bin/env python

"""
Technic ServerCore v0.1
Copyright (c) 2013 Syndicate, LLC <http://www.technicpack.net/>
"""

import sys, os, traceback, argparse
import time
import re
import json
import urllib, urllib2
import pprint

from Modpack import SolderPack
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed

def main ():

    global args

    if args.verbose: print sys.argv
    if args.listPacks:
	if len(sys.argv) > 2:
	    print "Error: Too many args"
            sys.exit(2)     
	else:
 	    listPacks()
    if args.modpack:
	if len(sys.argv) == 2:
	    displayPack(args.modpack)
	elif len(sys.argv) >= 4:
	    if args.install:
	        installPack(args.modpack, args.install)
            elif args.update:
	        print
            elif args.wipe:
                print
	

def getPacks ():

    global availPacks, mirrorURL
    rawJSON = urllib2.urlopen('http://solder.technicpack.net/api/modpack').read()
    solderJSON = json.loads(rawJSON)
    mirrorURL = solderJSON['mirror_url']
    availPacks = solderJSON['modpacks']

def getPackInfo (pack):

    global currentPack
    currentPack = SolderPack()
    rawJSON = urllib2.urlopen('http://solder.technicpack.net/api/modpack/' + pack).read()
    modpackJSON = json.loads(rawJSON)
    if 'error' in modpackJSON:
        print "Invalid Modpack: No modpack found"
        sys.exit(3)
    currentPack.setModpack(
        modpackJSON['display_name'], modpackJSON['name'], modpackJSON['url'], modpackJSON['recommended'], modpackJSON['latest'], modpackJSON['builds'])
  

def displayPack (pack):

    getPackInfo(pack)
    currentPack.printModpack()

def installPack (pack, build):

    getPackInfo(pack)
    if pack == 'attack-of-the-bteam':
        url = "http://mirror.technicpack.net/Technic/servers/bteam/BTeam_Server_v" + build + ".zip"
	print "\n\rDownlading build: " + build + " of " + currentPack.name + "\n\r"
	zipDir = os.getcwd() + '/serverZips/'
	zipFile = zipDir + build + '.zip'
	if not os.path.exists(zipDir):
	    os.makedirs(zipDir)

	widgets = ['Test: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets)
	
	def dlProgress(count, blockSize, totalSize):
	    if pbar.maxval is None:
        	pbar.maxval = totalSize
        	pbar.start()

	    pbar.update(min(count*blockSize, totalSize))
	
	urllib.urlretrieve(url, zipFile, reporthook=dlProgress)
	pbar.finish()

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
        parser.add_argument ('-ls', '--listPacks', action='store_true', default=False, help='list all available modpacks')
	parser.add_argument ('--install', action='store', metavar='<build>', help='install the currently selected server build')	
	parser.add_argument ('--update', action='store', metavar='<build>', help='update the currently selected server build')
	parser.add_argument ('--wipe', action='store', metavar='<build>', help='wipe and install the currently seleceted server build')
        parser.add_argument ('modpack', nargs='?',  action='store', help='determines which pack to use')
        parser.add_argument ('-v', '--version', action='version', version=globals()['__doc__'])
	parser.add_argument ('--verbose', action='store_true', default=False, help='verbose output')
        args = parser.parse_args()
        if not len(sys.argv) > 1:
            parser.error ('Missing argument')
        if args.verbose: print time.asctime()
	getPacks()
	main()
        if args.verbose: print time.asctime()
        if args.verbose: print 'TOTAL TIME IN SECONDS:',
        if args.verbose: print (time.time() - start_time)
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except urllib2.HTTPError, e: # no json found
	print 'Error: No JSON found'
	sys.exit(4)
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
