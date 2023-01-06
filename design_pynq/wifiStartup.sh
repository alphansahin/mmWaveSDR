#!/bin/bash

. /etc/environment
for f in /etc/profile.d/*.sh; do source $f; done

cc /home/xilinx/jupyter_notebooks/aerpaw/usbreset.c -o /home/xilinx/jupyter_notebooks/aerpaw/usbreset
chmod +x /home/xilinx/jupyter_notebooks/aerpaw/usbreset
echo $(lsusb)
sudo /home/xilinx/jupyter_notebooks/aerpaw/usbreset /dev/bus/usb/001/003 
echo "reset 1"

BOOT_PY=/home/xilinx/jupyter_notebooks/aerpaw/wifiStartup.py

if test -f "$BOOT_PY"; then
    python3 $BOOT_PY
fi

sudo /home/xilinx/jupyter_notebooks/aerpaw/usbreset /dev/bus/usb/001/003 
echo "reset 2"