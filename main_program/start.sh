#!/usr/bin/env bash

#place this in /etc/init.d/ dir on pi
#run sudo update-rc.d /etc/init.d/nameofscript.sh defaults to enable it
#dont forget to chmod +x it

cd /home/pi/speedo/main_program
python3 run_forever.py speedometer.py