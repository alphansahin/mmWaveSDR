from librarySDR import *
from libraryCommunications import *
from mainDefaults import *
from time import time
import os
clear = lambda: os.system('cls')
clear()


parameters = {'verbose': False, \
              'IP': '192.168.10.2'}
sdr = objSDR(parameters)

3
ppdu = objPPDU(parametersPPDU)       

###################### Sweep TX beam index
IQtone = np.exp(1j*np.pi*2*np.linspace(0,5,50))
IQramp = np.linspace(0,1,50)
syncAndTestPreamble = np.concatenate((sdr.syncWaveform, np.zeros(50), 1j*IQramp, np.zeros(25), IQtone,  np.zeros(20)))

sdr.setFrequency(parametersDefault['fc'])
sdr.getFrequency()
sdr.setMode('RXen0_TXen1')

while True:
    t1=time();
    for beamIndexTX in np.arange(0,64,1):
        sdr.setTXBeamIndex(beamIndexTX)
        IQppdu = ppdu.encode(dec2bin(beamIndexTX,8)) 
        sdr.transmitIQData( np.concatenate((syncAndTestPreamble,IQppdu)) )
    elapsed = time() - t1
    print(elapsed)


sdr.setMode('RXen0_TXen0')


if False: # basic reception
    mode = 0
    numIQdataSamplesPerTransfer = 2**10
    sdr.setupReception(mode,numIQdataSamplesPerTransfer)

    sdr.setMode('RXen1_TXen0')

    numberOfTransfers = 1
    IQdataRX = sdr.receiveIQData(numberOfTransfers)         
    plt.figure(20)
    plt.title('Raw IQ data')
    ind = (np.arange(0,len(IQdataRX[0]),1))
    plt.plot(ind,IQdataRX[0].real)
    plt.show(block=False)
    plt.plot(ind,IQdataRX[0].imag)
    plt.show(block=False)
    plt.grid()
    plt.xlabel('Sample index')
    plt.ylabel('Amplitude')
    plt.show(block=False)

    sdr.setMode('RXen1_TXen0')
    print('Basic RX is done')

if False: # basic transmission
    sdr.setMode('RXen0_TXen1')
    sdr.transmitIQData(sdr.syncWaveform)         
    sdr.setMode('RXen0_TXen0')
    print('Basic TX is done')