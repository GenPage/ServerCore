#!/usr/bin/env python

"""
Technic ServerCore v0.3.0-alpha
Copyright (c) 2013-2014 Syndicate, LLC <http://www.technicpack.net/>
"""

import sys, os, traceback, argparse, errno
import time, shutil, pprint
import json, zipfile
import urllib, urllib2


from Modpack import SolderPack
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed

def main():

    global args
    global zipsOutput
    zipsOutput = '~/TechnicServerCore/servers/'

    if args.verbose: print sys.argv
    if args.listPacks:
        if args.verbose:
            if len(sys.argv) > 3:
                parser.error(" Too many args")
                sys.exit(2)
            else:
                listPacks()
        else:
            if len(sys.argv) > 2:
                    parser.error(" Too many args")
                    sys.exit(2)
            else:
                listPacks()
    elif args.modpack:
        if not args.verbose:
            if len(sys.argv) == 2:
                displayPack(args.modpack)
            elif len(sys.argv) == 3:
                if args.download:
                    if 'all' in args.modpack:
                        downloadAllPacks(args.download)
                    else:
                        downloadPack(args.modpack, args.download)
            elif len(sys.argv) == 4:
                if args.install:
                    sys.stdout.write("Install directory: [" + os.path.expanduser(zipsOutput) + "] ")
                    choice = raw_input()
                    if not choice:
                        choice = os.path.expanduser(zipsOutput)
                    installPack(args.modpack, args.install, os.path.expanduser(choice))
                elif args.download:
                    if 'all' in args.modpack:
                        downloadAllPacks(args.download)
                    else:
                        downloadPack(args.modpack, args.download)
                elif args.wipe:
                    sys.stdout.write("Install directory: [" + os.path.expanduser(zipsOutput) + "] ")
                    choice = raw_input()
                    if not choice:
                        choice = os.path.expanduser(zipsOutput)
                    wipePack(args.modpack, args.wipe, os.path.expanduser(choice))
            elif len(sys.argv) > 4:
                parser.error("Too many args provided")
                sys.exit(2)
        elif args.verbose:
            if len(sys.argv) == 3:
                displayPack(args.modpack)
            elif len(sys.argv) == 4:
                if args.download:
                    if 'all' in args.modpack:
                        downloadAllPacks(args.download)
                    else:
                        downloadPack(args.modpack, args.download)
            elif len(sys.argv) == 5:
                if args.install:
                    sys.stdout.write("Install directory: [" + os.path.expanduser(zipsOutput) + "] ")
                    choice = raw_input()
                    if not choice:
                        choice = os.path.expanduser(zipsOutput)
                    installPack(args.modpack, args.install, os.path.expanduser(choice))
                elif args.download:
                    if 'all' in args.modpack:
                        downloadAllPacks(args.download)
                    else:
                        downloadPack(args.modpack, args.download)
                elif args.wipe:
                    sys.stdout.write("Install directory: [" + os.path.expanduser(zipsOutput) + "] ")
                    choice = raw_input()
                    if not choice:
                        choice = os.path.expanduser(zipsOutput)
                    wipePack(args.modpack, args.wipe, os.path.expanduser(choice))
            elif len(sys.argv) > 5:
                parser.error("Too many args provided")
                sys.exit(2)
    else:
        parser.error("No modpack provided")
        sys.exit(5)
	

def getBuild(build):
   
    if 'latest' in build:
        return str(currentPack.latest)
    elif 'recommended' in build:
        return str(currentPack.recommended)
    else:
        return str(build)

def getPacks():

    global availPacks, mirrorURL
    rawJSON = urllib2.urlopen('http://solder.technicpack.net/api/modpack').read()
    solderJSON = json.loads(rawJSON)
    mirrorURL = solderJSON['mirror_url']
    availPacks = solderJSON['modpacks']

def getPackInfo(pack):

    global currentPack
    currentPack = SolderPack()
    rawJSON = urllib2.urlopen('http://solder.technicpack.net/api/modpack/' + pack).read()
    modpackJSON = json.loads(rawJSON)
    if 'error' in modpackJSON:
        parser.error("Invalid Modpack - No modpack found")
        sys.exit(3)
    currentPack.setModpack(
        modpackJSON['display_name'], modpackJSON['name'], modpackJSON['url'], modpackJSON['recommended'], modpackJSON['latest'], modpackJSON['builds'])

def displayPack(pack):

    getPackInfo(pack)
    currentPack.printModpack()

def downloadAllPacks(build):

    print 'Downloading all available packs...'
    for key in availPacks:
        if ('latest' in build):
            downloadPack(key, 'latest')
        elif 'recommended' in build:
            downloadPack(key, 'recommended')
        else:
            downloadPack(key, build)

    print 'Downloading Complete.'

def downloadPack(pack, build):

    getPackInfo(pack)
    currentBuild = getBuild(build)
    packAvailable = True
    if pack == 'attack-of-the-bteam':
        url = "http://mirror.technicpack.net/Technic/servers/bteam/BTeam_Server_v" + currentBuild + ".zip"
    elif pack == 'tekkitmain':
        url = "http://mirror.technicpack.net/Technic/servers/tekkitmain/Tekkit_Server_v" + currentBuild + ".zip"
    elif pack == 'hexxit':
        url = "http://mirror.technicpack.net/Technic/servers/hexxit/Hexxit_Server_v" + currentBuild + ".zip"
    elif pack == 'tekkitlite':
        url = "http://mirror.technicpack.net/Technic/servers/tekkitlite/Tekkit_Lite_Server_" + currentBuild + ".zip"
    elif pack == 'tekkit':
        url = "http://mirror.technicpack.net/Technic/servers/tekkit/Tekkit_Server_" + currentBuild + ".zip"
    elif pack == 'bigdig':
        url = "http://mirror.technicpack.net/Technic/servers/bigdig/BigDigServer-v" + currentBuild + ".zip"
    elif pack == 'voltz':
        url = "http://mirror.technicpack.net/Technic/servers/voltz/Voltz_Server_v" + currentBuild + ".zip"
    else:
        print currentPack.name + " has been retired from the Technic Launcher and is no longer available."
        packAvailable = False
    

    if packAvailable == True:
        if currentBuild in currentPack.builds:
            if args.verbose: print url
            print "\n\rDownlading build: " + currentBuild + " of " + currentPack.name + "\n\r"
            serverDir = os.path.expanduser('~/TechnicServerCore/serverZips/' + currentPack.display_name)
            if args.verbose: print serverDir
            serverFile = serverDir + '/' + currentPack.display_name + '-v' + currentBuild + '.zip'
            if args.verbose: print serverFile
            if not os.path.exists(serverDir):
                print "Creating directory: " + serverDir
                os.makedirs(serverDir)

            if os.path.exists(serverFile):
                if confirmInput("Zip already downloaded. Do you wish to re-download?", "no"):
                    silentRemove(serverFile)
                    downloadFile(url, serverFile)
                else:
                    print "Download aborted! \n\r"
            else:
                downloadFile(url, serverFile)

            return serverFile
        else:
            print "Build " + currentBuild + " does not exist for " + currentPack.name

def installPack(pack, build, dest):

    serverFile = downloadPack(pack, build)
    currentBuild = getBuild(build)
    print "Installing build: " + currentBuild + " of " + currentPack.name + "\n\r"
    if(zipfile.is_zipfile(serverFile)):
        print "Verifying Zip integrity..."
	with zipfile.ZipFile(serverFile, 'r', zipfile.ZIP_DEFLATED, True) as serverZip:
            if(serverZip.testzip() == None):
                print "Checking for directory..."
                if not os.path.exists(dest):
                    print "Directory does not exist. Creating..."
                    if args.verbose: print dest
                    os.makedirs(dest)
		    print "Extracting server files..."
                    if args.verbose: pprint.pprint(serverZip.namelist())
		    serverZip.extractall(dest)
                else:
                    print "Error: Directory already exists. Please use --wipe"
                    sys.exit(8)
            else:
                print "Error: Zip integrity check failed. Please try again."
                sys.exit(5)
        print "Install complete"	

def wipePack(pack, build, dest):
    
    if os.path.exists(dest): 
        if confirmInput("Are you sure you want to wipe this directory?", "no"):
            print "Wiping directory: " + dest
            shutil.rmtree(dest)
            installPack(pack, build, dest)
        else:
            print "Aborting..."
            sys.exit(0)
    else:
        if confirmInput("Directory does not exist. Would you still like to install this server pack?", "no"):
            installPack(pack, build, dest)
        else:
            print "Aborting..."
            sys.exit(0)

def listPacks():

    print "\n\rModpacks:"
    print "==========="
    for key in availPacks:
        print '{0} ==> {1}'.format(availPacks[key], key)
    print
    print "\n\rMirror URL: " + mirrorURL
    print

def silentRemove(file):

    try:
	os.remove(file)
    except OSError as e:
	if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
	    raise

def downloadFile(url, file):

    displayFile = os.path.basename(file)
    widgets = [displayFile + ': ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets)

    def dlProgress(count, blockSize, totalSize):
        if pbar.maxval is None:
            pbar.maxval = totalSize
            pbar.start()

        pbar.update(min(count*blockSize, totalSize))

    urllib.urlretrieve(url, file, reporthook=dlProgress)
    pbar.finish()
    print "Download complete! Downloaded to: " + file + "\n\r"
            

def confirmInput(question, default):

    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=globals()['__doc__'])
        parser.add_argument ('-ls', '--listPacks', action='store_true', default=False, help='list all available modpacks')
        parser.add_argument ('--install', const='recommended', nargs='?', metavar=('<build>'), help='installs the provided server build')	
        parser.add_argument ('--download', const='recommended', nargs='?', metavar=('<build>'), help='downloads the provided server build')
        parser.add_argument ('--wipe', const='recommended', nargs='?', metavar=('<build>'), help='wipe and install the provided server build')
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
