#!/usr/bin/env bash

adb forward tcp:20175 tcp:50000

#TODO kill all gpsd

gpsd -b tcp://localhost:20175
