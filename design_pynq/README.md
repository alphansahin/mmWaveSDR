This folder consists of everthing that runs in PYNQ. The main file that needs to be running is aerpawAPI.py:

Steps:
1) Create a folder: home/xilinx/jupyter_notebooks/aerpaw/
2) Copy everything in this folder to the folder above
3) Install the python modules in "packagesToInstall"
4) Run the following command in the terminal: sudo fuser -k 8080/tcp; sudo fuser -k 8081/tcp; sudo fuser -k 8080/tcp; sudo fuser -k 8081/tcp; python3 aerpawAPI.py


To connect RFSoC2x2, you can use wifiStartup.py. After reboot, the USB port that Wi-Fi dongle is connected needs to be reset (I am not exactly sure why this is the case, however, it works). You don't need Wi-Fi to run the aerpawAPI.py.
