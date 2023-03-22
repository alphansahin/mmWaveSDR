#from xrfclk import *
#from pynq import allocate
import numpy as np
import socket
from pynq import Overlay
from pyftdi.ftdi import Ftdi
from aerpawFPGAController import *
from aerpawSiversController import *
from aerpawLibraryCommunications import *


class objNetworkInterface():
    def __init__(self):
        fsysref = 32
        fpl = 192
        frfdc = 1536
        decimation = 1
        tagBitStream = 'v47'
        tagLMK = 'v0'
        tagLMX = 'v0'
        
        self.bitStreamAERPAW = 'aerpawFPGA_' + str(fsysref) \
                                             + '_' + str(fpl) \
                                             + '_' + str(frfdc) \
                                             + '_D' + str(decimation) \
                                             + '_' + tagBitStream + '.bit'
        self.lmkParameters = {'fsysref': fsysref, 'fpl': fpl, 'tag': tagLMK}
        self.lmxParameters = {'fpl': fpl, 'frfdc': frfdc, 'tag': tagLMX}          
        
        self.folderAERPAW = '/home/xilinx/jupyter_notebooks/aerpaw/'
        print("Hello AERPAW User")
        print('=================================')
        print('=================================')
        print('AERPAW folder: ' + self.folderAERPAW)
        print('FPGA bitsteam: ' + self.bitStreamAERPAW)
        print('=================================')
        print('=================================')
        print('')

        if True:
            print("Starting the FPGA controller")
            overlay = Overlay(self.folderAERPAW+self.bitStreamAERPAW)
            self.fgpaControllerObj = fgpaController(overlay,self.lmkParameters,self.lmxParameters)
            print("FPGA controller is loaded.")
            
        self.controlSiversFromRFSoC = True
        if self.controlSiversFromRFSoC == True:
            print("Starting Sivers EVK controller")
            allDevices=Ftdi.list_devices()
            Ftdi.show_devices()
            strFTDIdesc = str(allDevices[0][0])
            snStr = strFTDIdesc[strFTDIdesc.find('sn=')+4:strFTDIdesc.find('sn=')+14]
            siverEVKAddr = 'ftdi://ftdi:4232:'+ snStr
            print(siverEVKAddr)            
            self.siversControllerObj = siversController(siverEVKAddr)
            self.siversControllerObj.init()
            print("Sivers EVK controlloer is loaded")
             
        
        print("Starting TCP server")
        self.localIP = "0.0.0.0"
        self.bufferSize = 2**10
        
        ## Command 
        self.localPort = 8080
        self.TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)# Create a datagram socket
        self.TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.TCPServerSocket.bind((self.localIP, self.localPort)) # Bind to address and ip
        
        ## Data
        self.localPortData = 8081
        self.TCPServerSocketData = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)         # Create a datagram socket
        self.TCPServerSocketData.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.TCPServerSocketData.bind((self.localIP, self.localPortData))                # Bind to address and ip

        bufsize = self.TCPServerSocketData.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) 
        print ("Buffer size [Before]:%d" %bufsize)  
        
        #SEND_BUF_SIZE = 4096*8
        #self.TCPServerSocketData.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)    
        #bufsize = self.TCPServerSocketData.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) 
        #print ("Buffer size [After]:%d" %bufsize)         
        
        print("TCP server up...")

        ## Default definitions
        Nsidelobes = int(20)
        Noversampling = int(4)
        rho = 0.5
        NrepeatSDRTrigger = int(4)
        Ga = np.array([1,1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,-1,1,1,1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,1,-1])
        syncWaveform = fcn_singleCarrier(rho, np.tile(Ga,NrepeatSDRTrigger), Noversampling, Nsidelobes)
        self.syncWaveform = syncWaveform/np.max(syncWaveform)        


        
    def run(self):
        # Listen for incoming connections
        self.TCPServerSocket.listen(1)
        self.TCPServerSocketData.listen(1)
        
        while True:
            # Wait for a connection
            print ('\nWaiting for a connection')
            self.connectionCMD, addrCMD = self.TCPServerSocket.accept()
            self.connectionData, addrDATA = self.TCPServerSocketData.accept()
            
            after_idle_sec=1
            interval_sec=3
            max_fails=5
            self.connectionData.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.connectionData.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
            self.connectionData.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
            self.connectionData.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)
            
            self.connectionCMD.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.connectionCMD.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
            self.connectionCMD.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
            self.connectionCMD.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)            
            
            try:
                while True:
                    try:
                        receivedCMD = self.connectionCMD.recv(self.bufferSize)
                        if receivedCMD:
                            print("\nClient CMD:{}".format(receivedCMD.decode()))
                            responseToCMDinBytes = self.parseAndExecute(receivedCMD)
                            self.connectionCMD.sendall(responseToCMDinBytes)
                        else:
                            break
                    except:
                        break
            finally:
                # Clean up the connection
                print('\nConnection is closed.')
                if self.controlSiversFromRFSoC == True:
                    self.siversControllerObj.setMode('RXen0_TXen0')
                self.connectionCMD.close()                  
                self.connectionData.close() 
                
    def parseAndExecute(self, receivedCMD):
        clientMsg = receivedCMD.decode()
        invalidCommandMessage = "ERROR: Invalid command"
        invalidNumberOfArgumentsMessage = "ERROR: Invalid number of arguments"
        successMessage = "Successully executed"
        droppedMessage = "Connection dropped?"
        clientMsgParsed = clientMsg.split()
        
        #######################
        if clientMsgParsed[0] == "setupReception":
            if len(clientMsgParsed) == 3:
                modeRX = int(clientMsgParsed[1])
                numIQdataSamplesPerTransfer = int(clientMsgParsed[2])
                success, status = self.fgpaControllerObj.setup_reception(modeRX, numIQdataSamplesPerTransfer, isRawFormat=True)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status                    
            else:
                responseToCMD = invalidNumberOfArgumentsMessage
                
        elif clientMsgParsed[0] == "getNumberOfAvailableTransfers":
            if len(clientMsgParsed) == 1:
                responseToCMD = str(self.fgpaControllerObj.numberOfAvailableTransfers)
            else:
                responseToCMD = invalidNumberOfArgumentsMessage       
                
        elif clientMsgParsed[0] == "setTransferEnableRXFlag":
            if len(clientMsgParsed) == 2:
                val = clientMsgParsed[1]
                success, status = self.fgpaControllerObj.setTransferEnableRXFlag(val)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status 
            else:
                responseToCMD = invalidNumberOfArgumentsMessage                         
                 
                
        elif clientMsgParsed[0] == "receiveIQSamples":
            if len(clientMsgParsed) == 3:
                numberOfTransfers = int(clientMsgParsed[1])
                timeOut = float(clientMsgParsed[2])
                success, status, iq_data = self.fgpaControllerObj.receive(numberOfTransfers,timeOut)
                if success == True:
                        self.connectionData.sendall(iq_data.tobytes())  
#                     remaining = len(iq_data)
#                     blockSize = 512
#                     start = 0
#                     while remaining>0:
#                         if remaining > blockSize:
#                             stop = start + blockSize
#                             remaining = remaining - blockSize        
#                         else:
#                             stop = start+remaining
#                             remaining = 0
#                         print(start)
#                         self.connectionData.send(iq_data[start:stop].tobytes())                            
#                         start = stop
                        
                responseToCMD = status
            else:
                responseToCMD = invalidNumberOfArgumentsMessage
                
        #######################
        elif clientMsgParsed[0] == "transmitIQSamples":
            if len(clientMsgParsed) == 2:
                numIQdataSamples = int(clientMsgParsed[1])
                IQdataInBytes = bytearray()
                self.connectionData.setblocking(True)
                connectionDropped = False
                while len(IQdataInBytes) < numIQdataSamples*4:
                    packet = self.connectionData.recv(numIQdataSamples*4 - len(IQdataInBytes))
                    if len(packet) == 0:
                        connectionDropped = True
                        responseToCMD = droppedMessage
                        print(droppedMessage)
                        break
                    else:
                        IQdataInBytes.extend(packet)
                        
                if connectionDropped == False:
                    IQdataInINT16 =  np.frombuffer(IQdataInBytes, np.int16)
                    success, status = self.fgpaControllerObj.transmit(IQdataInINT16,True)
                    if success == True:
                        responseToCMD = successMessage
                    else:
                        responseToCMD = status
                    
            else:
                responseToCMD = invalidNumberOfArgumentsMessage    
                
        #######################
        elif clientMsgParsed[0] == "getFGPABitStreamFileName":
            if len(clientMsgParsed) == 1:
                responseToCMD = self.bitStreamAERPAW
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
                
        #######################  
        elif clientMsgParsed[0] == "getRegisters":
            if len(clientMsgParsed) == 1:
                responseToCMD = self.fgpaControllerObj.monitor[0].readMonitorRegisters()
            else:
                responseToCMD = invalidNumberOfArgumentsMessage         
        #######################        

                
        #######################        
        elif clientMsgParsed[0] == "getBeamIndexTX":
            if len(clientMsgParsed) == 1:
                responseToCMD = str(self.siversControllerObj.getBeamIndexTX())
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setBeamIndexTX":
            if len(clientMsgParsed) == 2:
                beamIndex = int(clientMsgParsed[1])
                success, status = self.siversControllerObj.setBeamIndexTX(beamIndex)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status 
            else:
                responseToCMD = invalidNumberOfArgumentsMessage       
                
                
        #######################        
        elif clientMsgParsed[0] == "getBeamIndexRX":
            if len(clientMsgParsed) == 1:
                responseToCMD = str(self.siversControllerObj.getBeamIndexRX())
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setBeamIndexRX":
            if len(clientMsgParsed) == 2:
                beamIndex = int(clientMsgParsed[1])
                success, status = self.siversControllerObj.setBeamIndexRX(beamIndex)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status 
            else:
                responseToCMD = invalidNumberOfArgumentsMessage                    
                
        #######################        
        elif clientMsgParsed[0] == "getModeSiver":
            if len(clientMsgParsed) == 1:
                responseToCMD = self.siversControllerObj.getMode()
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setModeSiver":
            if len(clientMsgParsed) == 2:
                mode = clientMsgParsed[1]
                success,status = self.siversControllerObj.setMode(mode)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status                  
            else:
                responseToCMD = invalidNumberOfArgumentsMessage   
                
        #######################        
        elif clientMsgParsed[0] == "getGainRX":
            if len(clientMsgParsed) == 1:
                rx_gain_ctrl_bb1, rx_gain_ctrl_bb2, rx_gain_ctrl_bb3, rx_gain_ctrl_bfrf,agc_int_bfrf_gain_lvl, agc_int_bb3_gain_lvl = self.siversControllerObj.getGainRX()
                responseToCMD = 'rx_gain_ctrl_bb1:' + str(hex(rx_gain_ctrl_bb1)) + \
                                ', rx_gain_ctrl_bb2:' +  str(hex(rx_gain_ctrl_bb2)) + \
                                ', rx_gain_ctrl_bb3:' +   str(hex(rx_gain_ctrl_bb3)) + \
                                ', rx_gain_ctrl_bfrf:' +   str(hex(rx_gain_ctrl_bfrf)) +\
                                ', agc_int_bfrf_gain_lvl:' +   str(hex(agc_int_bfrf_gain_lvl)) +\
                                ', agc_int_bb3_gain_lvl:' +   str(hex(agc_int_bb3_gain_lvl))
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setGainRX":
            if len(clientMsgParsed) == 5:
                rx_gain_ctrl_bb1 = int(clientMsgParsed[1])
                rx_gain_ctrl_bb2 = int(clientMsgParsed[2])
                rx_gain_ctrl_bb3 = int(clientMsgParsed[3])
                rx_gain_ctrl_bfrf = int(clientMsgParsed[4])
                
                success,status = self.siversControllerObj.setGainRX(rx_gain_ctrl_bb1, rx_gain_ctrl_bb2, rx_gain_ctrl_bb3, rx_gain_ctrl_bfrf)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status                  
            else:
                responseToCMD = invalidNumberOfArgumentsMessage                 
                
        #######################        
        elif clientMsgParsed[0] == "getGainTX":
            if len(clientMsgParsed) == 1:
                tx_bb_gain, tx_bb_phase, tx_bb_iq_gain, tx_bfrf_gain, tx_ctrl = self.siversControllerObj.getGainTX()
                responseToCMD = 'tx_bb_gain:' + str(hex(tx_bb_gain)) + \
                                ', tx_bb_phase:' +  str(hex(tx_bb_phase)) + \
                                ', tx_bb_gain:' +   str(hex(tx_bb_iq_gain)) + \
                                ', tx_bfrf_gain:' +   str(hex(tx_bfrf_gain)) + \
                                ', tx_ctrl:' +   str(hex(tx_ctrl))
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setGainTX":
            if len(clientMsgParsed) == 5:
                print(clientMsgParsed[1])
                
                tx_bb_gain = int(clientMsgParsed[1])
                tx_bb_phase = int(clientMsgParsed[2])
                tx_bb_iq_gain = int(clientMsgParsed[3])
                tx_bfrf_gain = int(clientMsgParsed[4])
                
                success,status = self.siversControllerObj.setGainTX(tx_bb_gain, tx_bb_phase, tx_bb_iq_gain, tx_bfrf_gain)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status                  
            else:
                responseToCMD = invalidNumberOfArgumentsMessage     
                
        #######################        
        elif clientMsgParsed[0] == "getCarrierFrequency":
            if len(clientMsgParsed) == 1:
                responseToCMD = str(self.siversControllerObj.getFrequency())
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setCarrierFrequency":
            if len(clientMsgParsed) == 2:
                print(clientMsgParsed[1])
                fc = float(clientMsgParsed[1])
                success, status = self.siversControllerObj.setFrequency(fc)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status 
            else:
                responseToCMD = invalidNumberOfArgumentsMessage
                
        #######################        
        elif clientMsgParsed[0] == "getAWVTX":
            if len(clientMsgParsed) == 2:
                index = int(clientMsgParsed[1])
                responseToCMD = ','.join(str(x) for x in self.siversControllerObj.getAWVTX(index))
                print(responseToCMD)
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setAWVTX":
            if len(clientMsgParsed) == 34:
                print(clientMsgParsed[1])
                print(clientMsgParsed[2:])
                index = int(clientMsgParsed[1])
                awv = [int(i) for i in clientMsgParsed[2:]]
                #print(index)
                #print(awv)
                success, status = self.siversControllerObj.setAWVTX(index,awv)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status 
            else:
                responseToCMD = invalidNumberOfArgumentsMessage          
                
        #######################        
        elif clientMsgParsed[0] == "getAWVRX":
            if len(clientMsgParsed) == 2:
                index = int(clientMsgParsed[1])
                responseToCMD = ','.join(str(x) for x in self.siversControllerObj.getAWVRX(index))
                print(responseToCMD)
            else:
                responseToCMD = invalidNumberOfArgumentsMessage 
        elif clientMsgParsed[0] == "setAWVRX":
            if len(clientMsgParsed) == 34:
                print(clientMsgParsed[1])
                print(clientMsgParsed[2:])
                index = int(clientMsgParsed[1])
                awv = [int(i) for i in clientMsgParsed[2:]]
                #print(index)
                #print(awv)
                success, status = self.siversControllerObj.setAWVRX(index,awv)
                if success == True:
                    responseToCMD = successMessage 
                else:
                    responseToCMD = status 
            else:
                responseToCMD = invalidNumberOfArgumentsMessage          
                
        #######################
        else:
            responseToCMD = invalidCommandMessage    
            
        
        responseToCMDInBytes = str.encode(responseToCMD + " (" + clientMsg + ")" )  
        return responseToCMDInBytes
        
    
    
    
networkInterfaceObj = objNetworkInterface()
networkInterfaceObj.run()