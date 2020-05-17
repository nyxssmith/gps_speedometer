#!/bin/bash

#!/usr/bin/env bash

#place this in /etc/init.d/ dir on pi
#run sudo update-rc.d /etc/init.d/nameofscript.sh defaults to enable it
#dont forget to chmod +x it

cd /home/pi/gps_speedometer/v2
cp speedo.py temp.py
python3 run_forever.py temp.py
