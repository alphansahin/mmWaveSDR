from librarySDR import *
from libraryCommunications import *
from mainDefaults import *
from time import sleep
from matplotlib.pyplot import figure, draw, pause, colorbar
from scipy.io import savemat

import os
clear = lambda: os.system('cls')
clear()

parametersRX = {'verbose': True, \
              'IP': '192.168.10.5'}
sdr = objSDR(parametersRX)


ppdu = objPPDU(parametersPPDU)       




#####################
mode = 1
numIQdataSamplesPerTransfer = (ppdu.Ncp + ppdu.Nidft)*4 + 300
sdr.setupReception(mode, numIQdataSamplesPerTransfer)
sdr.setMode('RXen1_TXen0')
sdr.getMode()

sdr.setFrequency(parametersDefault['fc'])
sdr.getFrequency()


# SNRbeam = -30*np.ones((64,64))
# fg = figure(10)
# ax = fg.gca()
# ax.set_title('SNR [dB] matrix')
# ax.set_xlabel('TX beam index')
# ax.set_ylabel('RX beam index')
# ax.set_xlim([0,63])
# ax.set_ylim([0,63])
# im = ax.imshow(SNRbeam, extent=[0,63,63,0],cmap='jet', vmin=-30, vmax=30)
# cbar = colorbar(im)
# draw(), pause(1e-3) 

loc = 'loc1'
testID = 'lab_f' + str(int(parametersDefault['fc']/1e7)) + '_' + loc
for beamIndexRX in np.arange(0,64,1):
    sdr.setRXBeamIndex(beamIndexRX)
    sdr.enableTransfers()
    #pause(0.1), draw(), 
    sleep(2.2)
    sdr.disableTransfers()
    Navailable = sdr.getNumberOfAvailableTransfer() 
    

    if Navailable>0:
        IQdataRX = sdr.receiveIQData(Navailable)
        savemat('measurement_'+ testID + '_indexRX' + str(beamIndexRX) + '.mat', {'IQdata': IQdataRX, 'beamIndexRX': beamIndexRX, 'testID': testID})
        
        # for indTransfer in range(Navailable):
        #     IQdataChosen = IQdataRX[indTransfer]

        #     ppduInfo = ppdu.decode(IQdataChosen, parametersDefault['fs'], parametersDefault['Nstart'], debug=False)

        #     if ppduInfo['isValid'] == 1:
        #         beamIndexTXdetected = bin2dec(ppduInfo['dataBits'],isSigned=False)
        #         print(' > CFO...............:' + str(ppduInfo['fcfoEst']))
        #         print(' > SNR [dB]..........:' + str(ppduInfo['SNRdBEst']))
        #         print(' > Detected beamindex:' + str(beamIndexTXdetected))
        #         if beamIndexTXdetected<64:
        #             SNRbeam[beamIndexRX,beamIndexTXdetected] = ppduInfo['SNRdBEst']
        #             im.set_data(SNRbeam)
                    
        #     else:
        #         print(ppduInfo['reason'])
        #     print('-------------------------')  
    else:     
        IQdataRX = np.nan
        savemat('measurement_'+ testID + '_indexRX' + str(beamIndexRX) + '.mat', {'IQdata': IQdataRX, 'beamIndexRX': beamIndexRX, 'testID': testID})
    


# plt.savefig(testID+'_snrMatrix.eps', bbox_inches='tight', pad_inches=0.0, dpi=200,)
# plt.savefig(testID+'_snrMatrix.png', bbox_inches='tight', pad_inches=0.0, dpi=200,)

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