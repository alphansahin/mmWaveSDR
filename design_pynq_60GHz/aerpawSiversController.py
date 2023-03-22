import pickle
from pyftdi.spi import SpiController
from aerpawSiversCommon import *
from aerpawSiversDefaults import *

class siversController(siversDefaults):
    import time
    def __init__(self,siverEVKAddr):
        siversDefaults.__init__(self)
        ctrlA= SpiController(cs_count=1)
        ctrlA.configure(siverEVKAddr+'/1') 
        self.spiSiver = ctrlA.get_port(cs=0, freq=60E6, mode=0)

        ctrlB= SpiController()#spi
        ctrlB.configure(siverEVKAddr+'/2') 
        self.gpioB = ctrlB.get_gpio()
        self.gpioB.set_direction(0xF0,0xF0)  #[RST_N, PWR_EN, X, X, Xspi, Xspi, Xspi, Xspi]      
        self.gpioB.write(0x00)
        self.reset()
       
    def reset(self):
        # Reset EVK
        self.gpioB.write(0x00) # reset:On, power: Off
        self.gpioB.write(0x40) # reset:On, power: On
        #gpio1.write(0x80) # reset:Off, power: off
        self.gpioB.write(0xC0) # reset:Off, power: on        

    def init(self):
        self.reset()

        # Bias the circuitries
        self.wr('bias_ctrl',0x7f) # Enable all the biases
        self.wr('bias_pll',0x17)  # Enable all the biases for PPL with nominal current
        self.wr('bias_lo',0x2a)   # Set nominal bias for X3  (TX,RX,X3)       
        if self.chipType == 'Eder B MMF':
            self.wr('bias_tx',  0x96aa)
            self.wr('bias_rx', 0x0aa9)
            if (self.fc <= self.bias_vco_x3_lo_freq) or (self.frequency >= self.bias_vco_x3_hi_freq):
                self.wr('bias_vco_x3',0x02)
            else:
                self.wr('bias_vco_x3',0x01)            
        else:
            self.wr('bias_tx',  0xaeaa)        
            self.wr('bias_rx',  0xaaaa)
            self.wr('bias_vco_x3',0x00) # X3 out bias

        # Enable reference
        self.wr('fast_clk_ctrl',0x20) # Ref Clk = 45 MHz, Fast CLK freq = 180 MHz

        # Initialize ADC
        self.tgl('adc_ctrl',0x20) # reset ADC with toggling
        adc_sample_clk=19e6; cycle=10; set_edge=0
        fast_clk_ctrl_reg = self.rd('fast_clk_ctrl') & 0x10
        if fast_clk_ctrl_reg == 0x10:
            freq = self.freq * 5
        elif fast_clk_ctrl_reg == 0x00:
            freq = self.freq * 4 
        div = int(((38 * adc_sample_clk) / freq) - 1)
        self.wr('adc_clk_div',div)
        self.wr('adc_sample_cycle',cycle)
        if (set_edge == 1):
            self.set('adc_ctrl',2)
        else:
            self.clr('adc_ctrl',2)  

        # AGC:
        self.wr('gpio_agc_gain_in_ctrl',0x80)
        self.wr('gpio_agc_start_ctrl',0x00)
        self.wr('gpio_tx_rx_sw_ctrl',0x00)
        
        # Enable PLL/VCO
        self.wr('pll_en',0x7b)                                              # Enable PLL
        self.wr('pll_ref_in_lvds_en',0x01)                                  # LVDS input
        self.wr('pll_chp',0x01)                                             # Set charge pump current to 600 uA
        self.wr('vco_alc_del',0x0e)                                         # 311 nanoseconds
        self.wr('vco_tune_loop_del',0x000384)                               # 20 microseconds
        self.wr('vco_atc_vtune_set_del',0x001194)                           # 100 microseconds
        self.wr('vco_atc_vtune_unset_del',0x000384)                         # 20 microseconds
        self.wr('vco_override_ctrl',0x3f)                                   # Internal VCO tune state machine
        self.wr('vco_vtune_ctrl',0x20)                                      # ATC Low threshold mux function enabled
        self.alc_th=int(self.alc_th_v/self.dac_ref*255)                     # VCO amplitude threshold
        self.wr('vco_alc_hi_th', self.alc_th)
        self.atc_hi_th=int(self.atc_hi_th_v/self.dac_ref*255)
        self.wr('vco_atc_hi_th', self.atc_hi_th)
        self.atc_lo_th=int(self.atc_lo_th_v/self.dac_ref*255)
        self.wr('vco_atc_lo_th',self.atc_lo_th)
        self.wr('pll_pfd',0x00)                                             # Enable PFD Test
        self.wr('vco_en',0x3c)
        self.set('vco_tune_ctrl',0xFF)
        self.clr('vco_tune_ctrl',0xFF)

        restart = True
        if restart == True:
            self.set('vco_tune_ctrl',(1<<2))
        else:
            self.clr('vco_tune_ctrl',(1<<2))  
        self.time.sleep(0.5)                
        self.wr('vco_en',0x3c) # Enable VCO

        # Set Carrier Frequency
        self.setFrequency(self.fc)
        
        # Initialize RX/TX
        self.wr('trx_rx_on', 0x1FFFFF)
        self.wr('rx_gain_ctrl_mode', 0x13) # Direct register control
        self.wr('rx_gain_ctrl_sel', 0x3ff)
        self.wr('rx_bb_biastrim',0x00) # nominal current bias
        self.wr('rx_bb_test_ctrl',0xd9)
        self.wr('rx_dco_en',0x01)
        self.wr('rx_bb_i_dco',0x101b)
        self.wr('rx_bb_q_dco',0x1076)
        self.wr('rx_drv_dco',0xff0305ff)        
       
        self.wr('rx_gain_ctrl_bb1',0x77) # I[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps, Q[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps
        self.wr('rx_gain_ctrl_bb2',0x11) # I[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps, Q[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps
        self.wr('rx_gain_ctrl_bb3',0x44) # I[0:3]:[0-F]:0:6 dB, 16 steps, Q[0:3]:[0-F]:0:6 dB, 16 steps, 
        self.wr('rx_gain_ctrl_bfrf',0x77) # this is the gain before RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16 steps
        self.wr('rx_gain_ctrl_reg_index',0x0)
        
        self.wr('trx_tx_on',0x1FFFFF)
        self.wr('tx_ctrl', 0x18)
        self.wr('tx_bb_i_dco',0x2f) # Nominal: 0x40
        self.wr('tx_bb_q_dco',0x35) # Nominal: 0x40
        self.wr('tx_alc_ctrl',0x80) # adjust RF gain before BF gain (ALC is off)
        self.wr('tx_bb_gain', 0x00) # tx_ctrl bit 3 (BB Ibias set) = 0: 0x00  = 0 dB, 0x01  = 6 dB, 0x02  = 6 dB, 0x03  = 9.5 dB
                                    # tx_ctrl bit 3 (BB Ibias set) = 1, 0x00  = 0 dB, 0x01  = 3.5 dB, 0x02  = 3.5 dB, 0x03  = 6 dB *
        self.wr('tx_bb_phase', 0x00)
        self.wr('tx_bb_iq_gain', 0x44) # this is the gain in BB, [0:3,I gain]: 0-6 dB, 16 steps, [4:7, Q gain]: 0-6 dB, 16 steps
        self.wr('tx_bfrf_gain', 0x33)  # this is the gain after RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16 steps        

        # Set the AWVs
        if True:
            self.loadDumb('aerpawDefaultConf',group='bf_rx')
            #siversControllerObj.dump(group='bf_rx', isDetailed = False)
            self.loadDumb('aerpawDefaultConf',group='bf_tx')
            #siversControllerObj.dump(group='bf_tx', isDetailed = False)  
            
        self.setBeamIndexTX(32)
        self.setBeamIndexRX(32)
        
        
    def getGainRX(self):
        rx_gain_ctrl_bb1 = self.rd('rx_gain_ctrl_bb1')
        rx_gain_ctrl_bb2 = self.rd('rx_gain_ctrl_bb2')
        rx_gain_ctrl_bb3 = self.rd('rx_gain_ctrl_bb3')
        rx_gain_ctrl_bfrf = self.rd('rx_gain_ctrl_bfrf')
        agc_int_bfrf_gain_lvl = self.rd('agc_int_bfrf_gain_lvl')
        agc_int_bb3_gain_lvl = self.rd('agc_int_bb3_gain_lvl')
        
        return rx_gain_ctrl_bb1, rx_gain_ctrl_bb2, rx_gain_ctrl_bb3, rx_gain_ctrl_bfrf, agc_int_bfrf_gain_lvl, agc_int_bb3_gain_lvl
    
    def setGainRX(self,rx_gain_ctrl_bb1,rx_gain_ctrl_bb2,rx_gain_ctrl_bb3,rx_gain_ctrl_bfrf):
        if rx_gain_ctrl_bb1>255 or rx_gain_ctrl_bb1<0 or \
            rx_gain_ctrl_bb2>255 or rx_gain_ctrl_bb2<0 or \
            rx_gain_ctrl_bb3>255 or rx_gain_ctrl_bb3<0 or \
            rx_gain_ctrl_bfrf>255 or rx_gain_ctrl_bfrf<0:
            success = False
            status = "Gain values should between 0 and 255." 
            return success, status
        
        self.wr('rx_gain_ctrl_bb1',rx_gain_ctrl_bb1) 
        self.wr('rx_gain_ctrl_bb2',rx_gain_ctrl_bb2) 
        self.wr('rx_gain_ctrl_bb3',rx_gain_ctrl_bb3) 
        self.wr('rx_gain_ctrl_bfrf',rx_gain_ctrl_bfrf) 
        success = True
        status = "Success"        
        return success, status
    
        
    def getGainTX(self):
        tx_bb_gain = self.rd('tx_bb_gain')
        tx_bb_phase = self.rd('tx_bb_phase')
        tx_bb_iq_gain = self.rd('tx_bb_iq_gain')
        tx_bfrf_gain = self.rd('tx_bfrf_gain')
        tx_ctrl = self.rd('tx_ctrl')
        return tx_bb_gain, tx_bb_phase, tx_bb_iq_gain, tx_bfrf_gain, tx_ctrl
    
    def setGainTX(self,tx_bb_gain,tx_bb_phase,tx_bb_iq_gain,tx_bfrf_gain):
        if tx_bb_gain>255 or tx_bb_gain<0 or \
            tx_bb_phase>255 or tx_bb_phase<0 or \
            tx_bb_iq_gain>255 or tx_bb_iq_gain<0 or \
            tx_bfrf_gain>255 or tx_bfrf_gain<0:
            success = False
            status = "Gain values should between 0 and 255." 
            return success, status
        
        self.wr('tx_bb_gain',tx_bb_gain)
        self.wr('tx_bb_phase',tx_bb_phase)
        self.wr('tx_bb_iq_gain',tx_bb_iq_gain)
        self.wr('tx_bfrf_gain',tx_bfrf_gain)
        success = True
        status = "Success"        
        return success, status

    def getMode(self):
        self.mode = self.rd('trx_ctrl') & 0x03
        if self.mode == 0:
            mode = 'RXen0_TXen0'
        elif self.mode == 1:
            mode = 'RXen1_TXen0'
        elif self.mode == 2:
            mode = 'RXen0_TXen1'
        elif self.mode == 3:
            mode = 'RXen1_TXen1'
        return mode

    def setMode(self, mode):
        if mode == 'RXen0_TXen0':
            self.wr('trx_ctrl',0x00)
            success = True
            status = "Success"            
        elif mode == 'RXen1_TXen0':
            self.wr('trx_ctrl',0x01)
            success = True
            status = "Success"              
        elif mode == 'RXen0_TXen1':
            self.wr('trx_ctrl',0x02)
            success = True
            status = "Success"              
        elif mode == 'RXen1_TXen1':
            #self.wr('trx_ctrl',0x03) # dangerous case
            print('Not performed.')
            success = False
            status = "Not implemented"  
        else:
            success = False
            status = "No such mode. Only available modes are RXen0_TXen0,RXen1_TXen0,RXen0_TXen1."  
            
        return success,status
            
    def freq_to_divn(self, freq):
        return int(freq/6/self.freq-36)

    def divn_to_freq(self, divn):
        return (divn+36)*6*self.freq

    def getFrequency(self): 
        divn = self.rd('pll_divn')  
        return self.divn_to_freq(divn)     

    def setFrequency(self, frequency):
        if frequency > 70e9 or frequency < 57.51e9:
            success = False
            status = "ERROR: Invalid carrier frequency"
            return success, status
        
        print('Setting frequency to {} GHz'.format(frequency/1e9))
        start_time = self.time.time()

        self.t=self.getTemperature('K')-273
        # Set vco amplitude according to temperature 
        self.alc_th=int((self.alc_th_v + (25-self.t)*2.4e-3)/self.dac_ref*255)  # VCO amplitude threshold
        self.wr('vco_alc_hi_th', self.alc_th)        
        if self.chipType == 'Eder B MMF':
            #Set vtune_th according to temperature
            self.vtune_th=int((self.t*9e-3+1.166)*255/self.dac_ref)
            #pll_chp is set to 0x01 before lock
            self.clr('pll_chp', 0x03)
            self.set('pll_chp', 0x01)
        else:
            self.vtune_th=int((self.t*67e-4+1.066)*255/self.dac_ref)
        print('Temperature: ' + "%1.3f" % (self.t) + ' C')
        print('vco_vtune_atc_lo_th: ' + hex(self.vtune_th) + ' (' + "%1.3f" % (self.vtune_th*self.dac_ref/255) + ' V)')
        print('vco_tune_ctrl: ' + hex(self.rd('vco_tune_ctrl')))
        self.wr('vco_vtune_atc_lo_th',self.vtune_th)
        self.wr('pll_divn',self.freq_to_divn(frequency))
        self.tgl('vco_tune_ctrl', 0x02)
        self.tgl('vco_tune_ctrl', 0x01)
        self.time.sleep(0.002) 									# Increased to 2 ms from 0.5 ms
        vco_tune_status = self.rd('vco_tune_status')
        vco_tune_det_status = self.rd('vco_tune_det_status')
        vco_tune_freq_cnt = self.rd('vco_tune_freq_cnt')
        print('vco_tune_status [0x7e]: ' + hex(vco_tune_status))
        print('vco_tune_det_status[0] [1]: ' + hex(vco_tune_det_status))
        print('vco_tune_freq_cnt [0x7ff +/-11]: ' + hex(vco_tune_freq_cnt))
        if self.chipType == 'Eder B MMF':
            #Set pll_chp to 0x00 if digtune between 28 and 64 or 92 and 128
            digtune=self.rd('vco_tune_dig_tune')
            if (0x5C < digtune) or (0x1D < digtune < 0x40):
                self.clr('pll_chp', 0x03)
        # Check if tuning has succeeded
        if (vco_tune_status != 0x7e) or \
           (vco_tune_det_status & 0x01 != 0x01) or \
           (vco_tune_freq_cnt > 0x80a) or \
           (vco_tune_freq_cnt < 0x7f4):
            print('VCO tune FAILED')
        else:
            print('VCO tune OK.')
            self.set('vco_tune_ctrl', 0x04)

        success = True
        status = "Success"
        return success, status            
        

    def setBeamIndexTX(self, index):
        if index > 63 or index<0:
            success = False
            status = 'ERROR: TX beam index should be between 0 and 63'
            return success, status
        else:
            ptr = 0x80 | index
            success = True
            status = 'Success'            
            self.wr('bf_tx_awv_ptr', ptr)
            return success, status        
        

    def setBeamIndexRX(self, index):
        if index > 63 or index<0:
            success = False
            status = 'ERROR: RX beam index should be between 0 and 63'
            return success, status
        else:
            ptr = 0x80 | index
            success = True
            status = 'Success'            
            self.wr('bf_rx_awv_ptr', ptr)
            return success, status

    def getBeamIndexTX(self):
        return 0x7F & self.rd('bf_tx_awv_ptr')

    def getBeamIndexRX(self):
        return 0x7F & self.rd('bf_rx_awv_ptr')
    

    ## ADC
    def getTemperatureRaw(self):
        self.startADC(src1 = 0x83,src2 = None,log2_nsamples = 4)
        temp = self.meanADC()
        self.stopADC()
        return temp

    def getTemperature(self,unit='C'):
        return self.getTemperatureRaw()*self.temp_scale - self.temp_comp + self.unit_offs[unit] + self.temp_calib_offset

    def startADC(self,src1, src2=None, log2_nsamples=4):
        #self.lock.acquire()
        if (self.rd('adc_ctrl') & 0x80) == 0x80:
            print('ADC has been started and is ready, but has not been stopped/reseted.')
            return
        self.__src_1, self.__src_2 = self.getAMUX()
        self.setAMUX(src1,src2)
        self.wr('adc_num_samples', log2_nsamples)
        self.tgl('adc_ctrl',0x10)
        while (self.rd('adc_ctrl') & 0x80) == 0:
            pass

    def stopADC(self):
        self.tgl('adc_ctrl',0x20)        
        self.setAMUX(self.__src_1,self.__src_2)

    def meanADC(self):
        return self.rd('adc_mean') & 0x0fff

    def maxADC(self):
        return self.rd('adc_max') & 0x0fff

    def minADC(self):
        return self.rd('adc_min') & 0x0fff
    
    def diffADC(self):
        return self.rd('adc_diff') & 0x0fff

    ## AMUX
    def setAMUX(self, src=None, src_2=None):
        """Enables output of source "src" on AMUX-pin.
           src : source for AMUX output
           Example:
           amux.set(dbg.amux_vco)
        """
        if src != None:
            self.wr('bist_amux_ctrl',src)

        if src_2 != None:
            if   (self.rd('bist_amux_ctrl') & 0x7F) == self.amux_rx_bb:
                self.wr('rx_bb_test_ctrl', src_2)
            elif (self.rd('bist_amux_ctrl') & 0x7F) == self.amux_vco:
                self.wr('vco_amux_ctrl', src_2)
            elif (self.rd('bist_amux_ctrl') & 0x7F) == self.amux_otp:
                self.wr('bist_ot_ctrl', src_2)
            elif (self.rd('bist_amux_ctrl') & 0x7F) == self.amux_tx_pdet:
                self.wr('tx_bf_pdet_mux', src_2)
            elif (self.rd('bist_amux_ctrl') & 0x7F) == self.amux_tx_env_pdet:
                self.wr('tx_bf_pdet_mux', src_2)

    def getAMUX(self):
        src = self.rd('bist_amux_ctrl')
        src_2 = None
        if (0x7F & src) == (0x7F & self.amux_rx_bb):
            src_2 = self.rd('rx_bb_test_ctrl')
        elif (0x7F & src) == (0x7F & self.amux_vco):
            src_2 = self.rd('vco_amux_ctrl')
        elif (0x7F & src) == (0x7F & self.amux_otp):
            src_2 = self.rd('bist_ot_ctrl')
        elif (0x7F & src) == (0x7F & self.amux_tx_pdet):
            src_2 = self.rd('tx_bf_pdet_mux')
        elif (0x7F & src) == (0x7F & self.amux_tx_env_pdet):
            src_2 = self.rd('tx_bf_pdet_mux')
        return src, src_2

    def enableAMUX(self):
        """Enable output on AMUX-pin.
        """
        self.set('bist_amux_ctrl',0x80)

    def disableAMUX(self):
        """Disable output on AMUX-pin.
        """
        self.clr('bist_amux_ctrl',0x80)

    def clrAMUX(self):
        """Disable output on AMUX-pin.
        """
        self.clr('bist_amux_ctrl',0x80)    

    ## SPI      
    def getAddressAndSize(self,regKey):
        address = self.regs[regKey]['addr']
        size = self.regs[regKey]['size']   
        return address, size
        
    def rd(self,regKey):
        address, size = self.getAddressAndSize(regKey)
        command  = int2intlist((address << 3) + self.SPI_RD,256,2)
        read_buf = self.spiSiver.exchange(command,2+size,start=True, stop=True, duplex=True)
        read_buf = read_buf[2:]
        #print(self.fhex(self.intlist2int(read_buf),size))
        #print(''.join('{:02X}'.format(a) for a in list(read_buf)))
        #print(hex(int.from_bytes(read_buf,'big', signed=False)))
        return intlist2int(list(read_buf))
    
    def wr(self,regKey,data):
        address, size = self.getAddressAndSize(regKey)  
        data = int2intlist(data,num_ints=size)
        command = int2intlist((address << 3) + self.SPI_WR_RAW,256,2)
        data.append(0)
        self.spiSiver.write(command+data,start=True, stop=True) 
        
    def clr(self,regKey,data):
        address, size = self.getAddressAndSize(regKey) 
        command = int2intlist((address << 3) + self.SPI_WR_CLR,256,2)
        data = int2intlist(data,num_ints=size)
        data.append(0)
        self.spiSiver.write(command+data,start=True, stop=True) 
        
    def set(self,regKey,data):
        address, size = self.getAddressAndSize(regKey) 
        command = int2intlist((address << 3) + self.SPI_WR_SET,256,2)
        data = int2intlist(data,num_ints=size)
        data.append(0)
        self.spiSiver.write(command+data,start=True, stop=True)         

    def tgl(self,regKey,data):
        address, size = self.getAddressAndSize(regKey) 
        command = int2intlist((address << 3) + self.SPI_WR_TGL,256,2)
        data = int2intlist(data,num_ints=size)
        data.append(0)
        self.spiSiver.write(command+data,start=True, stop=True)   

    def dump(self, group='', isDetailed ='False'):
        selectedDict = self.regs 
        print('===========================')     
        if group != '':
            for regKey in (selectedDict):
                if selectedDict[regKey]['group'] == group:
                    data = self.rd(regKey)
                    print(regKey + ':'+ hex(data))
                    if isDetailed:
                        print(selectedDict[regKey]['doc'] )
                        print('\n')
        else:
            for regKey in (selectedDict):
                data = self.rd(regKey)
                print(regKey + ':'+ hex(int.from_bytes(data,'big', signed=False)))
                if isDetailed:
                    print(selectedDict[regKey]['doc'] )
                    print('\n')    
        print('\n')
            
    def dumpSave(self, filename, group=''):
        save_list = []
        if group != '':
            for regKey in (self.regs):
                if self.regs[regKey]['group'] == group:
                    data = self.rd(regKey)
                    save_list.append([regKey, data])
            pickle.dump(save_list,open(filename+'_'+group, "wb"))     
        else:
            for regKey in (self.regs):
                data = self.rd(regKey)
                save_list.append([regKey, data])
            pickle.dump(save_list,open(filename+'_allRegs', "wb"))     
          
    def loadDumb(self, filename, group=''):
        if group != '':
            load_list = pickle.load(open(filename+'_'+group, "rb"))   
        else:      
            load_list = pickle.load(open(filename+'_allRegs', "rb"))      
        for regKey in (load_list):
            self.wr(regKey[0],regKey[1]) 
    