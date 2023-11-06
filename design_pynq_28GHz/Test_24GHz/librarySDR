import socket
from libraryCommunications import *



class objSDR:
    def __init__(self, parameters):
        ##################################### General #####################################
        localIP = parameters['IP']  # The server's hostname or IP address
        self._verbose = parameters['verbose']  # verbose
        localPort = 8080  # The port used by the server
        self.clientControlRadio = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)# Create a datagram socket
        self.clientControlRadio.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientControlRadio.connect((localIP, localPort)) # Bind to address and ip

        localPort = 8081  # The port used by the server
        self.clientDataRadio = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)# Create a datagram socket
        self.clientDataRadio.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientDataRadio.connect((localIP, localPort)) # Bind to address and ip      

        Nsidelobes = int(20)
        Noversampling = int(4)
        rho = 0.2
        NrepeatSDRTrigger = int(4)
        Ga = np.array([1,1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,-1,1,1,1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,1,-1])
        self.syncWaveform = fcn_singleCarrier(rho, np.tile(Ga,NrepeatSDRTrigger), Noversampling, Nsidelobes)        
    
        fc = 24.00e9
        self.setFrequency(fc)  
        self.setMode('RXen0_TXen0')
        self.getMode()

        ##################################### Transmitter #####################################
        self.setTXGain()
        self.getTXGain()
        self.setTXBeamIndex(0)
        self.getTXBeamIndex()

        ##################################### Receiver  #####################################
        self.getMonitorRegisters()
        self.setupReception(0, 128)
        self.setRXGain()
        self.getRXGain()
        self.setRXBeamIndex(0)
        self.getRXBeamIndex()        


        print('SDR initialization is done.')
        print('========================')

    def setVerbose(self, verboseFlag):
        self._verbose = verboseFlag

    def setMode(self, mode):
        if mode == 'RXen0_TXen1' or mode == 'RXen1_TXen0' or mode == 'RXen0_TXen0':
            self.clientControlRadio.sendall(b"setModeSiver "+str.encode(str(mode)))
            data = self.clientControlRadio.recv(1024)
            if self._verbose:
                print(data)  

    def getMode(self):
        self.clientControlRadio.sendall(b"getModeSiver")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data

    def setupReception(self, mode = 0, numIQdataSamplesPerTransfer = 128):
        self.clientControlRadio.sendall(b"setupReception " + str.encode(str(mode)) + b" " + str.encode(str(numIQdataSamplesPerTransfer)))
        data = self.clientControlRadio.recv(1024)
        self._numIQdataSamplesPerTransfer = numIQdataSamplesPerTransfer
        if self._verbose:
            print(data) 
        return data       

    def disableTransfers(self):
        self.clientControlRadio.sendall(b"setTransferEnableRXFlag 0")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data   

    def enableTransfers(self):
        self.clientControlRadio.sendall(b"setTransferEnableRXFlag 1")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data               

    def setFrequency(self, fc):
        self.clientControlRadio.sendall(b"setCarrierFrequency "+str.encode(str(fc)))
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data

    def getFrequency(self):
        self.clientControlRadio.sendall(b"getCarrierFrequency")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return float((data.split()[0]))

    def setTXGain(self):
        if False: # defaults
            tx_bb_gain = 0x00;  # 0x00  = 0 dB, 0x01  = 3.5 dB, 0x02  = 3.5 dB, 0x03  = 6 dB
            tx_bb_phase = 0x0; 
            tx_bb_iq_gain = 0x00; # The gain in BB, [I gain]: 0-6 dB (0:F),  [Q gain]: 0-6 dB (0:F)
            tx_bfrf_gain = 0x7F # The gain after RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16 steps        
        else: # New settings
            tx_bb_gain = 0x03;  # 0x00  = 0 dB, 0x01  = 3.5 dB, 0x02  = 3.5 dB, 0x03  = 6 dB
            tx_bb_phase = 0x00; 
            tx_bb_iq_gain = 0x03; # The gain in BB, [I gain]: 0-6 dB (0:F),  [Q gain]: 0-6 dB (0:F)
            tx_bfrf_gain = 0x7F # The gain after RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16 steps        

        self.clientControlRadio.sendall(b"setGainTX " + str.encode(str(int(tx_bb_gain)) + " ") \
                                                    + str.encode(str(int(tx_bb_phase)) + " ") \
                                                    + str.encode(str(int(tx_bb_iq_gain)) + " ") \
                                                    + str.encode(str(int(tx_bfrf_gain))) \
                )
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data 

    def getTXGain(self):
        self.clientControlRadio.sendall(b"getGainTX")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data

    def setRXGain(self):
        if False: # defaults
            rx_gain_ctrl_bb1 = 0x00; # I[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB, Q[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB
            rx_gain_ctrl_bb2 = 0x00; # I[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB, Q[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB
            rx_gain_ctrl_bb3 = 0x33; # I[0:3]:[0,1,3,7,F]: based on agc_int_bb3_gain_lvl, Q[0:3]: based on agc_int_bb3_gain_lvl
                                    # agc_int_bb3_gain_lvl:0xfca752 => {2,5,7,10,12,15}/3 = {0,1,2,3,4,5} dB
            rx_gain_ctrl_bfrf = 0x7F # RF gain[0:3]:[0,1,3,7,F]: based on agc_int_bfrf_gain_lvl, [4:7, BF gain]:[0,1,3,7,F]: based on agc_int_bfrf_gain_lvl
                                    # agc_int_bfrf_gain_lvl:0xffcc9966 => RF gain:{6,9,12,15} dB, BF gain:{6,9,12,15} dB
        else: # New settings
            rx_gain_ctrl_bb1 = 0x00; # I[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB, Q[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB
            rx_gain_ctrl_bb2 = 0x00; # I[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB, Q[0:3]:[0,1,3,7,F]:-6, 0, 6, 12, 18 dB
            rx_gain_ctrl_bb3 = 0x11; # I[0:3]:[0,1,3,7,F]: based on agc_int_bb3_gain_lvl, Q[0:3]: based on agc_int_bb3_gain_lvl
                                    # agc_int_bb3_gain_lvl:0xfca752 => {2,5,7,10,12,15}/3 = {0,1,2,3,4,5} dB
            rx_gain_ctrl_bfrf = 0x77 # RF gain[0:3]:[0,1,3,7,F]: based on agc_int_bfrf_gain_lvl, [4:7, BF gain]:[0,1,3,7,F]: based on agc_int_bfrf_gain_lvl
                                    # agc_int_bfrf_gain_lvl:0xffcc9966 => RF gain:{6,9,12,15} dB, BF gain:{6,9,12,15} dB

        self.clientControlRadio.sendall(b"setGainRX " + str.encode(str(int(rx_gain_ctrl_bb1)) + " ") \
                                                    + str.encode(str(int(rx_gain_ctrl_bb2)) + " ") \
                                                    + str.encode(str(int(rx_gain_ctrl_bb3)) + " ") \
                                                    + str.encode(str(int(rx_gain_ctrl_bfrf))) \
                )
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data       

    def getRXGain(self):
        self.clientControlRadio.sendall(b"getGainRX")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data       

    def setTXBeamIndex(self, beamIndexTX):
        self.clientControlRadio.sendall(b"setBeamIndexTX "+str.encode(str(beamIndexTX)))
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data  

    def getTXBeamIndex(self):
        self.clientControlRadio.sendall(b"getBeamIndexTX")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data          

    def setRXBeamIndex(self, beamIndexRX):
        self.clientControlRadio.sendall(b"setBeamIndexRX "+str.encode(str(beamIndexRX)))
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data     

    def getRXBeamIndex(self):
        self.clientControlRadio.sendall(b"getBeamIndexRX")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data 
     
#newly added to set AWVTX
    def setAWVTX(self, beamIndexTX, AWVTX):
        self.clientControlRadio.sendall(b"setAWVTX "+str.encode(str(beamIndexTX))+b" "+str.encode(str(AWVTX)))
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data     

    def getAWVTX(self, beamIndexTX):
        self.clientControlRadio.sendall(b"getAWVTX "+str.encode(str(beamIndexTX)))
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data 
            
#newly added to set AWVRX
    def setAWVRX(self, beamIndexRX, AWVRX):
        self.clientControlRadio.sendall(b"setAWVRX "+str.encode(str(beamIndexRX))+b" "+str.encode(str(AWVRX)))
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data   
    
    def pack_bytes_2_bf_awv(self, q, i):
        pack = lambda q , i : ( ((q & 0x3f) << 6) + (i & 0x3f) )
        return pack(q,i)
    
    def getNumberOfAvailableTransfer(self):
        self.clientControlRadio.sendall(b"getNumberOfAvailableTransfers")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data)         
        dataParsed = data.split()
        return int(dataParsed[0])        

    def transmitIQData(self, IQdataTX):
        numIQdataSamples = len(IQdataTX)
        self.clientControlRadio.sendall(b"transmitIQSamples "+str.encode(str(numIQdataSamples)))
        no_bits = 14
        inphase = (IQdataTX.real*(2**(no_bits-1)-1))
        inphase = inphase.astype('int16')
        quadrature = (IQdataTX.imag*(2**(no_bits-1)-1))
        quadrature = quadrature.astype('int16')

        # TX Buffer and plot
        iqTXbuf = np.empty((2*numIQdataSamples,), dtype=np.int16)
        iqTXbuf[0:numIQdataSamples] = inphase
        iqTXbuf[numIQdataSamples:2*numIQdataSamples] = quadrature
        self.clientDataRadio.sendall(iqTXbuf)
        data = self.clientControlRadio.recv(1024)
        #if self._verbose:
        #    print(data) 
        return data    

    def getMonitorRegisters(self):
        self.clientControlRadio.sendall(b"getRegisters")
        data = self.clientControlRadio.recv(1024)
        if self._verbose:
            print(data) 
        return data    

    def receiveIQData(self, numberOfTransfers, timeOut=2):
        self.clientControlRadio.sendall(b"receiveIQSamples "+str.encode(str(numberOfTransfers))  + b" " + str.encode(str(timeOut)) )
        expectedNumberOfBytes = self._numIQdataSamplesPerTransfer*numberOfTransfers*4
        IQdataInBytes = bytearray()
        #self.clientDataRadio.setblocking(True)
        while len(IQdataInBytes) < expectedNumberOfBytes:
            data = self.clientDataRadio.recv(expectedNumberOfBytes)
            IQdataInBytes.extend(data)
        dataIandQ = np.frombuffer(IQdataInBytes,dtype=np.int16)
        IQdataRX = dataIandQ[0:self._numIQdataSamplesPerTransfer*numberOfTransfers] + 1j*dataIandQ[self._numIQdataSamplesPerTransfer*numberOfTransfers:2*self._numIQdataSamplesPerTransfer*numberOfTransfers]
        no_bits = 12
        IQdataRX = 2**-(no_bits-1)*IQdataRX.astype(np.complex128)
        IQdataRX = IQdataRX.reshape(numberOfTransfers,self._numIQdataSamplesPerTransfer)

        data = self.clientControlRadio.recv(1024)
        #if self._verbose:
            #print(data) 
        return IQdataRX
