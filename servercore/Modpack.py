#!/usr/bin/env python

"""
Technic ServerCore v0.3.0-alpha
Copyright (c) 2013 Syndicate, LLC <http://www.technicpack.net/>
"""

import sys

class SolderPack:
    'This contains methods for a SolderPack object'
    name = None
    display_name = None
    url = None
    recommended = None
    latest = None
    builds = None

    def setModpack(self, name, display_name, url, recommended, latest, builds):
        self.name = name
        self.display_name = display_name 
        self.url = url
        self.recommended = recommended
        self.latest = latest
        self.builds = builds

    def printModpack(self):
	print '\n\rSelected Pack Info:'
	print '==========='
	print 'Name: ' + str(self.name)
	print 'Slug: ' + str(self.display_name)
	print 'URL: ' + str(self.url)
	print 
	print 'Builds:'
	print '-----------'
	print 'Recommended: ' + str(self.recommended)
	print 'Latest: ' + str(self.latest)
	sys.stdout.write('Builds: ')
        self.printBuilds()
	print '\n\r'
    


    def printBuilds(self):
	
	for build in self.builds:
	    if build == self.builds[-1]:
	        sys.stdout.write(str(build))
	    else:
	        sys.stdout.write(str(build) + ', ')
