from pynq.lib import Wifi

port = Wifi()

ssid = 'YourSSID'
pwd = 'YourPassword'
port.connect(ssid, pwd, True)