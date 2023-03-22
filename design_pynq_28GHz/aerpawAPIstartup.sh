#!/bin/bash

. /etc/environment
for f in /etc/profile.d/*.sh; do source $f; done

BOOT_PY=/home/xilinx/jupyter_notebooks/aerpaw/aerpawAPI.py
sudo fuser -k 8080/tcp
sudo fuser -k 8081/tcp

if test -f "$BOOT_PY"; then
   python3 $BOOT_PY
fi

