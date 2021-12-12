#!/bin/bash

# Switches between hotspot mode and a normal wireless connection
# usage hotspot.sh on|off

# Must run as root
if [[ $(id -u) -ne 0 ]] ; then 
	echo "Must sudo to run this script"
	exit 1
fi

if [ $# -lt 1 ] ; then
	echo "Usage: hotspot.sh on|off"
	exit 1
fi

case "$1" in
	on) echo "Turning on hotspot"; net="Astroberry HotSpot" ;;
	off) echo "Turning off hotspot, looking for home network"; net="Wireless connection" ;;
	*) "Usage: hotspot.sh on|off"; exit 1
esac

/usr/bin/nmcli -p con up "$net" ifname wlan0

echo "Done"
