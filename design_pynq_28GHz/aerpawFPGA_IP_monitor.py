from pynq import DefaultIP

class monitor(DefaultIP):
   
    def __init__(self, description):
        super().__init__(description=description)
        
    bindto = ['xilinx.com:ip:monitor:1.0']

    
    @property
    def timeStamp(self):
        return self.read(0x08)    

   
    @property
    def packetSizeTX(self):
        return self.read(0x100)
    
    @packetSizeTX.setter
    def packetSizeTX(self, packetsize):
        self.write(0x100, packetsize)
        
    @property
    def transferTriggerTX(self):
        return self.read(0x104)        
    
    @transferTriggerTX.setter
    def transferTriggerTX(self, transfer):
        if transfer:
            self.write(0x104, int(1))
        else:
            self.write(0x104, int(0))    
       
    @property
    def modeRX(self):
        return self.read(0x108)
    
    @modeRX.setter
    def modeRX(self, mode):
        self.write(0x108, mode)
        
    @property
    def transferSizeRX(self):
        return self.read(0x10C)
    
    @transferSizeRX.setter
    def transferSizeRX(self, packetsize):
        self.write(0x10C, packetsize)
 
    @property
    def transferTriggerRX(self):
        return self.read(0x110)
    
    @transferTriggerRX.setter
    def transferTriggerRX(self, transfer):
        if transfer:
            self.write(0x110, int(1))
        else:
            self.write(0x110, int(0))
   
    @property
    def stopFIFOCounter(self):
        return self.read(0x114)
    
    @stopFIFOCounter.setter
    def stopFIFOCounter(self, val):
        self.write(0x114, val)    
    
    
    @property
    def transferEnableRX(self):
        return self.read(0x118)
    
    @transferEnableRX.setter
    def transferEnableRX(self, transfer):
        if transfer:
            self.write(0x118, int(1))
        else:
            self.write(0x118, int(0))    
    
    @property
    def resetNumberOfTransfersCounterRX(self):
        return self.read(0x11C)
    
    @resetNumberOfTransfersCounterRX.setter
    def resetNumberOfTransfersCounterRX(self, inp):
        if inp:
            self.write(0x11C, int(1))
        else:
            self.write(0x11C, int(0))    
            
    def readMonitorRegisters(self):
        msg = 'packetSizeTX: '+str(self.packetSizeTX) +', ' \
            + 'transferTriggerTX: '+str(self.transferTriggerTX) +', ' \
            + 'modeRX: '+str(self.modeRX) +', ' \
            + 'transferSizeRX: '+str(self.transferSizeRX) +', ' \
            + 'transferEnableRX: '+str(self.transferEnableRX) +', ' \
            + 'transferTriggerRX: '+str(self.transferTriggerRX) +', ' \
            + 'detectedCntSingle: '+str(self.detectedCntSingle) +', ' \
            + 'detectedCntRepeat: '+str(self.detectedCntRepeat) +', ' \
            + 'cntDACFIFOI: '+str(self.cntDACFIFOI) +', ' \
            + 'cntDACFIFOQ: '+str(self.cntDACFIFOQ) +', ' \
            + 'cntADCFIFOI: '+str(self.cntADCFIFOI) +', ' \
            + 'cntADCFIFOQ: '+str(self.cntADCFIFOQ) +', ' \
            + 'stopFIFOCounter: '+str(self.stopFIFOCounter) +', ' \
            + 'systemRefCounter: '+str(self.systemRefCounter) +', ' \
            + 'numberOfTransfersRX: '+str(self.numberOfTransfersRX)
        return msg
    
    
    @property
    def detectedCntSingle(self):
        return self.read(0x200)           

    @property
    def detectedCntRepeat(self):
        return self.read(0x204)   
    
    @property
    def cntDACFIFOI(self):
        return self.read(0x208)       
    
    @property
    def cntDACFIFOQ(self):
        return self.read(0x20C)      
    
    @property
    def cntADCFIFOI(self):
        return self.read(0x210)       
    
    @property
    def cntADCFIFOQ(self):
        return self.read(0x214)  
    
    
    @property
    def systemRefCounter(self):
        return self.read(0x218)
    
    @property
    def numberOfTransfersRX(self):
        return self.read(0x21C)