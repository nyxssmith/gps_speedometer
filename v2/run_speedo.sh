#!/bin/bash

#!/usr/bin/env bash

#place this in /etc/init.d/ dir on pi
#run sudo update-rc.d /etc/init.d/nameofscript.sh defaults to enable it
#dont forget to chmod +x it

cd /home/pi/gps_speedometer/v2
python3 run_forever.py speedo.py
