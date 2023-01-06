from pynq.lib import Wifi

port = Wifi()

ssid = 'USRPnet'
pwd = 'BenSenOBizSizOnlar'
port.connect(ssid, pwd, True)