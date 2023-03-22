from pynq import DefaultIP
from pynq import allocate
import numpy as np
import aerpawFPGA_IP_RFCLK as xrfclk
import aerpawFPGA_IP_monitor as monitor
import aerpawFPGA_IP_DMA as dma
import aerpawFPGA_IP_SPI as spi
import aerpawFPGA_IP_RFDC as xrfdc
import time


    
class fgpaController():
    def __init__(self, overlay, lmkParameters, lmxParameters):
        
        self._isReceiveRunning = False
        
        # initials
        self._lmkParameters = lmkParameters
        self._lmxParameters = lmxParameters

        # IPs
        self.adcTileChannel = []
        self.adcBlockChannel = []
        self.dacTileChannel = []
        self.dacBlockChannel = []
        
        self.dmaRxRealChannel = []
        self.dmaRxImagChannel = []
        self.dmaTxRealChannel = []
        self.dmaTxImagChannel = []        
        
        self.rfdc = getattr(overlay, 'rfconverter').rfdc
        
        self.adcTileChannel.append(getattr(overlay.rfconverter, 'rfdc').adc_tiles[0])
        self.adcTileChannel.append(getattr(overlay.rfconverter, 'rfdc').adc_tiles[2])        
        
        self.dacTileChannel.append(getattr(overlay.rfconverter, 'rfdc').dac_tiles[0])
        self.dacTileChannel.append(getattr(overlay.rfconverter, 'rfdc').dac_tiles[1])        
        
        self.dmaRxRealChannel.append(getattr(overlay.receiverDMAs, 'axi_dma_adc0'))
        self.dmaRxImagChannel.append(getattr(overlay.receiverDMAs, 'axi_dma_adc2'))     
        
        self.dmaTxRealChannel.append(getattr(overlay.transmitterDMAs, 'axi_dma_dac0'))
        self.dmaTxImagChannel.append(getattr(overlay.transmitterDMAs, 'axi_dma_dac1'))          
        
        self.monitor = []
        self.monitor.append(getattr(overlay.rfconverter.controller, 'monitor_0'))
        
        # Setup
        self.setup_clk()
        self.setup_adcdac()
        
        self._numberOfPulls = 0
        self.setup_reception(modeRX=0, numIQdataSamplesPerTransfer=128, isRawFormat=True)     

        
    def setup_clk(self):   
        print('Setting the reference clocks for RF converters')
        xrfclk.set_ref_clks(self._lmkParameters, self._lmxParameters)
        time.sleep(0.5)
        print('Done.')
        print(' ')
        
    def setup_adcdac(self):
        """Configure the channels with default parameters
        """ 
   
        a=(self.monitor[0].systemRefCounter)  
        fref = self._lmkParameters['fsysref']*1e6;
        # Based on our tests, it is okay to set PL_SYSREF larger than 10 MHz and it seems working better
        print('A counter will run for 2 seconds assuming that PL_SYSREF is ' + str(fref/1e6) + ' MHz.')
        time.sleep(2) 
        b=(self.monitor[0].systemRefCounter)       
        tMeasured = np.float(((b-a) % 2**32) /fref)
        print('Measured value (this value should be closer to 5 seconds): ' + str(tMeasured))            
        if np.abs(tMeasured-2)>0.5:
            raise ValueError('It is off by more than 0.5 seconds. Check if PL_SYSREF is set to ' + str(fref/1e6) + '  MHz.')

        time.sleep(0.7) 
            
        self.rfdc.runMTS()
        self.rfdc.sysrefDisable() 
        time.sleep(0.5)                
            
        print('Setting up RF ADCs/DACs...')
        print('--------------------')
        
        for indChannel in range(len(self.adcTileChannel)):                  
            self.adcTileChannel[indChannel].blocks[0].ResetNCOPhase()        
            
        for indChannel in range(len(self.dacTileChannel)):                  
            self.dacTileChannel[indChannel].blocks[0].ResetNCOPhase()                 
        
        for indChannel in range(len(self.adcTileChannel)):   
            self.adcTileChannel[indChannel].blocks[0].MixerSettings = {
                'CoarseMixFreq':  xrfdc.COARSE_MIX_BYPASS,
                'EventSource':    xrfdc.EVNT_SRC_SYSREF,
                'FineMixerScale': xrfdc.MIXER_SCALE_0P7,
                'Freq': 0,
                'MixerMode':      xrfdc.MIXER_MODE_R2R,
                'MixerType':      xrfdc.MIXER_TYPE_COARSE,
                'PhaseOffset':    0.0} 
            
        for indChannel in range(len(self.dacTileChannel)): 
            self.dacTileChannel[indChannel].blocks[0].MixerSettings = {
                'CoarseMixFreq':  xrfdc.COARSE_MIX_BYPASS,
                'EventSource':    xrfdc.EVNT_SRC_SYSREF,
                'FineMixerScale': xrfdc.MIXER_SCALE_0P7,
                'Freq': 0,
                'MixerMode':      xrfdc.MIXER_MODE_R2R,
                'MixerType':      xrfdc.MIXER_TYPE_COARSE,
                'PhaseOffset':    0.0}
            
        for indChannel in range(len(self.adcTileChannel)): 
            self.adcTileChannel[indChannel].blocks[0].QMCSettings['EventSource'] = xrfdc.EVNT_SRC_SYSREF
            
        for indChannel in range(len(self.dacTileChannel)): 
            self.dacTileChannel[indChannel].blocks[0].QMCSettings['EventSource'] = xrfdc.EVNT_SRC_SYSREF                      
        for indChannel in range(len(self.adcTileChannel)):                  
            self.adcTileChannel[indChannel].SetupFIFO(True) 
            
        for indChannel in range(len(self.dacTileChannel)):                  
            self.dacTileChannel[indChannel].SetupFIFO(True)                    
           
        if True:
            for indChannel in range(len(self.adcTileChannel)):  
                print(['RX Channel ' + str(indChannel) + ' configuration:'])
                print('> Mixer settings: ' + str(self.adcTileChannel[indChannel].blocks[0].MixerSettings))
                print('> Block status: ' + str(self.adcTileChannel[indChannel].blocks[0].BlockStatus))
                print('> Decimation factor: '  + str(self.adcTileChannel[indChannel].blocks[0].DecimationFactor))
                print('> Mixer settings: ' + str(self.adcTileChannel[indChannel].blocks[0].MixerSettings))
                print('> PLL configs: ' + str(self.adcTileChannel[indChannel].PLLConfig))
                print('> QMC: ' + str(self.adcTileChannel[indChannel].blocks[0].QMCSettings))
                print(' ')

            for indChannel in range(len(self.dacTileChannel)):  
                print(['TX Channel ' + str(indChannel) + ' configuration:'])
                print('> Mixer settings: ' + str(self.dacTileChannel[indChannel].blocks[0].MixerSettings))
                print('> Block status: ' + str(self.dacTileChannel[indChannel].blocks[0].BlockStatus))
                print('> Interpolation factor: '  + str(self.dacTileChannel[indChannel].blocks[0].InterpolationFactor))
                print('> Mixer settings: ' + str(self.dacTileChannel[indChannel].blocks[0].MixerSettings))
                print('> PLL configs: ' + str(self.dacTileChannel[indChannel].PLLConfig))
                print('> QMC: ' + str(self.dacTileChannel[indChannel].blocks[0].QMCSettings))
                print(' ')            


        self.rfdc.sysrefEnable()   
        time.sleep(0.5)  
        self.rfdc.sysrefDisable() 
        print('Done.') 
        print(' ')

    def configuration_adc(self):
        """Configure the channels with default parameters
        """    
        print('Setting up RF ADCs')
        for indChannel in range(len(self.adcTileChannel)):
            print(['RX Channel ' + str(indChannel) + ' configuration:'])
            print('> Block status: ' + str(self.adcTileChannel[indChannel].blocks[0].BlockStatus))
            print('> Decimation factor: '  + str(self.adcTileChannel[indChannel].blocks[0].DecimationFactor))
            print('> Mixer settings: ' + str(self.adcTileChannel[indChannel].blocks[0].MixerSettings))
            print('> PLL configs: ' + str(self.adcTileChannel[indChannel].PLLConfig))
            print('> QMC: ' + str(self.adcTileChannel[indChannel].blocks[0].QMCSettings))                
                
                
    def transmit(self, iqData, isRawFormat):
        if len(iqData) > 2**18 or len(iqData) < 1:
            success = False
            status = 'ERROR: Number of IQ data samples should be in range 1 to 2^18.'
            return success, status        
        
        if isRawFormat == False: # Complex (Re/Im is between:-1 and 1)
            dataSize = len(iqData)
            inputBufferReal = allocate(shape=(dataSize,),dtype=np.int16)
            for i in range(len(IQdata)):
                inputBufferReal[i]= (IQdata[i].real*2**13).astype('int16')


            inputBufferImag = allocate(shape=(dataSize,),dtype=np.int16)
            for i in range(len(IQdata)):
                inputBufferImag[i]= (IQdata[i].imag*2**13).astype('int16') 
                
            self.dmaTxRealChannel[0].sendchannel.transfer(inputBufferReal)
            self.dmaTxImagChannel[0].sendchannel.transfer(inputBufferImag)

            self.monitor[0].packetSizeTX = dataSize//8
            self.monitor[0].transferTriggerTX = 0                
            self.monitor[0].transferTriggerTX = 1
        else: # INT16
            numberOfIQSamples = iqData.size//2
            transfersize = self.ceilDivision(numberOfIQSamples,8)
           
            inputBufferReal = allocate(shape=(transfersize*8,),dtype=np.int16)
            inputBufferReal[range(numberOfIQSamples)] = iqData[range(numberOfIQSamples)]
            inputBufferReal[range(numberOfIQSamples,transfersize*8)] = 0
            
            inputBufferImag = allocate(shape=(transfersize*8,),dtype=np.int16)
            inputBufferImag[range(numberOfIQSamples)] = iqData[range(numberOfIQSamples,iqData.size)]    
            inputBufferImag[range(numberOfIQSamples,transfersize*8)] = 0

            self.dmaTxRealChannel[0].sendchannel.transfer(inputBufferReal)
            self.dmaTxImagChannel[0].sendchannel.transfer(inputBufferImag)
            self.dmaTxRealChannel[0].sendchannel.wait()
            self.dmaTxImagChannel[0].sendchannel.wait()
            
            self.monitor[0].packetSizeTX = transfersize
            self.monitor[0].transferTriggerTX = 0 
            self.monitor[0].transferTriggerTX = 1
        
            success = True
            status = 'Success'
            return success, status 
        return success, status
    
    def setTransferEnableRXFlag(self, val):
        if val == '1':
            self.monitor[0].transferEnableRX = 1
            success = True
            status = "Success"            
        elif val == '0':
            self.monitor[0].transferEnableRX = 0
            success = True
            status = "Success"            
        else:
            success = False
            status = "No such option for the flag"            
        return success, status              
            
    def setup_reception(self, modeRX, numIQdataSamplesPerTransfer, isRawFormat):
        if numIQdataSamplesPerTransfer > 2**18 or numIQdataSamplesPerTransfer < 1:
            success = False
            status = 'ERROR: Number of IQ data samples should be in range 1 to 2^18.'
            return success, status
        
        if modeRX > 1:
            success = False
            status = "ERROR: Mode can be only 0 (only soft trigger) and 1 (soft and detector triggers)"
            return success, status
        
        # Flush the FIFOs

        Nflush = self.numberOfAvailableTransfers
        if Nflush>0:
            print('Ntransfer:'+str(self.monitor[0].numberOfTransfersRX))
            print('Npulls:'+str(self._numberOfPulls))                    
            print('Nflush:' + str(Nflush))
            self._pull(self.monitor[0].transferSizeRX*8, Nflush, isRawFormat=True)

        # Set the mode
        self.monitor[0].modeRX = modeRX
        
        # Disable transfers
        self.monitor[0].transferEnableRX = 0
        
        # Reset the transfer counter
        print('NtransferCNT:'+str(self.monitor[0].numberOfTransfersRX))
        print('Npulls:'+str(self._numberOfPulls))
        self.monitor[0].resetNumberOfTransfersCounterRX = 1
        self.monitor[0].resetNumberOfTransfersCounterRX = 0        
        
        # Set the transfer length
        transferSize = self.ceilDivision(numIQdataSamplesPerTransfer,8)
        self.monitor[0].transferSizeRX = transferSize 
        
        # Set the counter to declare no more reception
        self.monitor[0].stopFIFOCounter = int(np.floor(2**15/transferSize)*transferSize-4)-1
        
        # Enable transfers
        self.monitor[0].transferEnableRX = 1

        # Register the critical information for the reception
        self._numIQdataSamplesPerTransfer = numIQdataSamplesPerTransfer
        self._isRawFormat = isRawFormat
        self._modeRX = modeRX
        self._numberOfPulls = 0
        success = True
        status = "Success"
        
        print('NtransferCNT:'+str(self.monitor[0].numberOfTransfersRX))
        print('Npulls:'+str(self._numberOfPulls))        
        return success, status        
    
        
    def receive(self, numberOfTransfers, timeOut):
        numIQdataSamplesPerTransfer = self._numIQdataSamplesPerTransfer
        isRawFormat = self._isRawFormat
        modeRX = self._modeRX
        
        if numIQdataSamplesPerTransfer*numberOfTransfers > 2**18 or numIQdataSamplesPerTransfer*numberOfTransfers < 1:
            iq_data = np.array(0)
            success = False
            status = 'ERROR: Number of IQ data samples should be in range 1 to 2^18.'
            return success, status, iq_data
        
        if modeRX == 0:
            for indTrigger in range(numberOfTransfers):
                self._trigger()
            success, status, iq_data = self._pull(numIQdataSamplesPerTransfer, numberOfTransfers, isRawFormat)
            return success, status, iq_data
        
        if modeRX == 1:
            t1 = time.time()
            isCompletedOnTime = False
            while time.time()-t1<timeOut:
                Ncurrent = self.numberOfAvailableTransfers
                if Ncurrent >= numberOfTransfers:
                    isCompletedOnTime = True
                    break 

            if isCompletedOnTime == False:
                iq_data = np.empty(0)
                success = False
                status = 'ERROR: Waiting for the data. Only ' + str(Ncurrent) + '/' + str(numberOfTransfers) + ' transfers occurred so far.'
                return success, status, iq_data                  
            else: 
                success, status, iq_data = self._pull(numIQdataSamplesPerTransfer,numberOfTransfers,isRawFormat)
                return success, status, iq_data      
  
        
    def _trigger(self):
        self.monitor[0].transferTriggerRX = 0
        self.monitor[0].transferTriggerRX = 1
        
    def _pull(self, numIQdataSamplesPerTransfer, numberOfTransfers, isRawFormat):
        transferSize = self.ceilDivision(numIQdataSamplesPerTransfer,8)
        re_data = np.empty(0).astype('int16')
        im_data = np.empty(0).astype('int16')
        for indTransfer in range(numberOfTransfers):
            buffer_re = allocate(shape=(transferSize*8,), dtype=np.int16)
            buffer_im = allocate(shape=(transferSize*8,), dtype=np.int16)              
            t = time.time()
            self.dmaRxRealChannel[0].recvchannel.transfer(buffer_re)
            self.dmaRxImagChannel[0].recvchannel.transfer(buffer_im)
            self.dmaRxRealChannel[0].recvchannel.wait()
            self.dmaRxImagChannel[0].recvchannel.wait()
            self._numberOfPulls = self._numberOfPulls + 1
            elapsed = time.time() - t

            packetsize = transferSize*8
            print(indTransfer)
            print('DMA transfer rate: ' + str(packetsize/elapsed/1e+6) + ' Msps')
            print('Number of IQ samples: ' + str(packetsize))
            print('Elapsed time: ' + str(elapsed/1e-3) + ' ms')

            if isRawFormat == False: # Complex (Re/Im is between:-1 and 1)
                re_data = np.array(buffer_re)
                im_data = np.array(buffer_im)            
                re_data = re_data[0:numIQdataSamplesPerTransfer] * 2**-11
                im_data = im_data[0:numIQdataSamplesPerTransfer] * 2**-11  
                iq_dataPerTransfer =re_data.astype('double') + 1j * im_data.astype('double')
                iq_data = np.append(iq_data, iq_dataPerTransfer)                
            else: # INT16
                re_dataPerTransfer = np.array(buffer_re).astype('int16')
                im_dataPerTransfer = np.array(buffer_im).astype('int16')
                re_data =  np.append(re_data, re_dataPerTransfer[0:numIQdataSamplesPerTransfer])
                im_data =  np.append(im_data, im_dataPerTransfer[0:numIQdataSamplesPerTransfer])
                iq_data =  np.concatenate((re_data,im_data))
        buffer_re.freebuffer()
        buffer_im.freebuffer()
            
        success = True
        status = 'Success'            
        return success, status, iq_data

    def ceilDivision(self,a,b):
        return -(a // -b)

    @property
    def numberOfAvailableTransfers(self):
        return self.monitor[0].numberOfTransfersRX - self._numberOfPulls
    
    @property
    def sampleRateADC(self):
        # sample rate
        return self.adcTileChannel[0].blocks[0].BlockStatus['SamplingFreq']/self.adcTileChannel[0].blocks[0].DecimationFactor     

    @property
    def frequencyNCOADC(self):
        # sample rate
        return self.adcTileChannel[0].blocks[0].MixerSettings['Freq']    

    @property
    def decimationFactor(self):
        # sample rate
        return self.adcTileChannel[0].blocks[0].DecimationFactor    
