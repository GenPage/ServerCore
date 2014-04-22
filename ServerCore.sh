#!/bin/bash

#/**
# *
# *   Copyright © 2014 by Syndicate LLC 
# *   http://www.technicpack.net/
# *
# *   All rights reserved.
# *
# **/

CFG_FILE="ServerCore.config"

function sigQuit {
    echo
    quit
}

trap sigQuit SIGINT SIGTERM



