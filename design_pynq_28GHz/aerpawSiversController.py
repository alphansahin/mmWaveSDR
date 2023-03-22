import pickle
from pyftdi.spi import SpiController
from pyftdi.gpio import GpioAsyncController
from aerpawSiversCommon import *
from aerpawSiversDefaults import *

class siversController(siversDefaults):
    import time
    def __init__(self,siverEVKAddr):
        siversDefaults.__init__(self)

        # A SPI
        ctrlA= SpiController(cs_count=3)
        ctrlA.configure(siverEVKAddr+'/1') 
        self.spiSiver = ctrlA.get_port(cs=0, freq=10E6, mode=0)
        self.spiChronos = ctrlA.get_port(cs=2, freq=10E6, mode=0)


        # BGPIO - Power & reset
        ctrlB= SpiController()#spi
        ctrlB.configure(siverEVKAddr+'/2') 
        self.gpioB = ctrlB.get_gpio()
        self.gpioB.set_direction(0xF0,0xF0)  #[RST_N, PWR_ENb, X, PWR_ENa, Xspi, Xspi, Xspi, Xspi]   
                                             # First arg: pins, Second arg: Direction    1: Output, 0: Input   

 
        # CGPIO - Cruijff/Chronos select
        self.gpioC= GpioAsyncController()
        self.gpioC.configure(siverEVKAddr+'/3', direction=0xFF)   #[X, X, X, X, X, X, CS_chronos, X]  1: Output, 0: Input
        self.gpioC.write(0xFF) # select Cruijff   ; 0x00 for Chronos    
        
        self.reset()
       
    def reset(self):
        # Reset EVK
        self.gpioB.write(0x00) # reset:On, power: Off #[RST_N, PWR_ENb, X, PWR_ENa, Xspi, Xspi, Xspi, Xspi]    
        self.gpioB.write(0x50) # reset:On, power: On #[RST_N, PWR_ENb, X, PWR_ENa, Xspi, Xspi, Xspi, Xspi]    
        self.gpioB.write(0xD0) # reset:Off, power: On #[RST_N, PWR_ENb, X, PWR_ENa, Xspi, Xspi, Xspi, Xspi]      
        self.gpioC.write(0xFF) # select Cruijff   ; 0x00 for Chronos    
        
    def init(self):
        self.reset()
        
        # Bias the circuitries
        self.wr('bias_ctrl',0x7f) # Enable all the biases
        self.wr('bias_pll',0x17)  # Enable all the biases for PPL with nominal current
        self.wr('bias_lo',0x2a)   # Set nominal bias for X3  (TX,RX,X3)       
        self.wr('bias_tx',  0xaaaa)        
        self.wr('bias_rx',  0xaaa)
        self.wr('bias_vco_x3',0x02) # X3 out bias
        

        # System:
        self.wr('fast_clk_ctrl',0x50) #  184.32 MHz (dig_tune=0, divR=1, divN=3, ref freq=122.88 MHz)
        self.wr('gpio_tx_rx_sw_ctrl',0x00)
        self.wr('gpio_agc_start_ctrl',0x00)
        self.wr('gpio_agc_gain_in_ctrl',0x80)
        self.wr('gpio_agc_gain_out_ctrl',0x00)    
        
        # Initialize ADC
        self.tgl('adc_ctrl',0x31) # reset ADC with toggling
        self.wr('adc_clk_div',0x8)
        self.wr('adc_sample_cycle',0xa)
        self.wr('adc_num_samples',0x6)
        self.wr('adc_sample',0x10b)
        self.wr('adc_mean',0x0)
        self.wr('adc_max',0x0)
        self.wr('adc_min',0xfff)
        self.wr('adc_diff',0x0)
       
        

        # VCO/PLL enable
        self.wr('vco_override_ctrl',0x3f)
        self.wr('bias_vco_x3',0x02)
        self.set('bias_ctrl',0x7f)                                          # Enable BG and LDO:s
        self.wr('bias_pll',0x07)                                            # Set PLL bias till 80% of nominal current
        self.wr('bias_lo',0x2a)                                             # Set nominal bias for X3
        self.set('pll_en',0x08)                                             # Enable LD
        self.wr('vco_en', 0x09)                                             # Enable External LO Buffer in and X3 buffer out

        # Set Carrier Frequency
        self.setFrequency(self.fc)

        # Initialize RX/TX
        self.wr('trx_rx_on', 0x1FFFFF)
        self.wr('rx_gain_ctrl_mode', 0x13) # Direct register control
        self.wr('rx_gain_ctrl_sel', 0x3ff)
        self.wr('rx_bb_biastrim',0x00) # nominal current bias
        self.wr('rx_bb_test_ctrl',0xd9)
        self.wr('rx_dco_en',0x0) # No DC comp
        self.wr('rx_bb_i_dco',0x3f) # Nominal: 0x3f
        self.wr('rx_bb_q_dco',0x3f) # Nominal: 0x3f
    

        # default RX gains
        self.wr('rx_gain_ctrl_bb1',0x77) # I[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps, Q[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps
        self.wr('rx_gain_ctrl_bb2',0x11) # I[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps, Q[0:3]:[0,1,3,7,F]:-6:0 dB, 4 steps
        self.wr('rx_gain_ctrl_bb3',0x44) # I[0:3]:[0-F]:0:6 dB, 16 steps, Q[0:3]:[0-F]:0:6 dB, 16 steps, 
        self.wr('rx_gain_ctrl_bfrf',0x77) # this is the gain before RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16 steps
        self.wr('rx_gain_ctrl_reg_index',0x0)

        self.wr('trx_tx_on',0x1FFFFF)
        self.wr('tx_ctrl', 0x18)
        self.wr('tx_bb_i_dco',0x40) # Nominal: 0x40
        self.wr('tx_bb_q_dco',0x40) # Nominal: 0x40
        self.wr('tx_alc_ctrl',0x80) # adjust RF gain before BF gain (ALC is off)
        
        # Default TX gains
        self.wr('tx_bb_gain', 0x00) # tx_ctrl bit 3 (BB Ibias set) = 0: 0x00  = 0 dB, 0x01  = 6 dB, 0x02  = 6 dB, 0x03  = 9.5 dB
                                    # tx_ctrl bit 3 (BB Ibias set) = 1, 0x00  = 0 dB, 0x01  = 3.5 dB, 0x02  = 3.5 dB, 0x03  = 6 dB *
        self.wr('tx_bb_phase', 0x00)
        self.wr('tx_bb_iq_gain', 0x44) # this is the gain in BB, [0:3,I gain]: 0-6 dB, 16 steps, [4:7, Q gain]: 0-6 dB, 16 steps
        self.wr('tx_bfrf_gain', 0x33)  # this is the gain after RF mixer, [0:3,RF gain]: 0-15 dB, 16 steps, [4:7, BF gain]: 0-15 dB, 16 steps                
            


        # Set the AWVs
        if False:
            self.loadDumb('aerpawDefaultConf',group='bf_rx')
            #siversControllerObj.dump(group='bf_rx', isDetailed = False)
            self.loadDumb('aerpawDefaultConf',group='bf_tx')
            #siversControllerObj.dump(group='bf_tx', isDetailed = False)  

        #self.setBeamIndexTX(32)
        #self.setBeamIndexRX(32)
        
        
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


    def getFrequency(self): 
        return self.fc     

    def setFrequency(self, frequency):
        if frequency > 29.5e9 or frequency < 24e9:
            success = False
            status = "ERROR: Invalid carrier frequency"
            return success, status            

        self.fc = frequency
        out_freq = frequency
        ref_freq = self.freq
        int_mode=False

        if int_mode:
            ref_div = 3
        else:
            ref_div = 2    #Set to 0 or 1 for reference < 60 MHz, 2 for reference = 122.88 MHz
        divn_div8_9 = 0
        en_x2_outamp = 1

        ref_div_arr = [ 1, 1, 2, 4]

        # "/ 3" since Chronos multiplies by 3
        tmp = ( ( out_freq / 3) / 2**en_x2_outamp) / ( ref_freq / ref_div_arr[ ref_div])

        nint_sd = int( tmp) - ( 20 + 16 * divn_div8_9)
        frac_sd = int( ( tmp - ( nint_sd + 20 + 16 * divn_div8_9)) * 2**16)
        nint = int(round(tmp) - ( 20 + 16 * divn_div8_9))

        self.actual_freq = ((ref_freq / ref_div) * (nint_sd + 20 + 16 * divn_div8_9 + (frac_sd / 65536.0)) * (2 - 1 * en_x2_outamp)) * 6


        print('  Setting Chronos with ref_freq = %d, ref_div = %d, divn_div8_9 = %d, en_x2_outamp = %d' % \
            ( ref_freq, ref_div, divn_div8_9, en_x2_outamp))

        # Tip: the dictionaries were obtained using chronos.printfmt( reg_name)
        self.wr_chronos(  3, self.dict2int( { 'addr':3 , 'ref_mode':1 , 'en_chp':1 , 'r_sel_ref':ref_div , 'en_leak':0 , 'divn_div8_9':divn_div8_9 , }))

        self.wr_chronos(  4, self.dict2int( { 'addr':4 , 'order_sd':0 , 'nint_sd':nint , }))
        if int_mode:
            self.wr_chronos(  5, self.dict2int( { 'addr':5 , 'frac_lsb_set':0 , 'frac_sd':0 , }))
        else:
            self.wr_chronos(  5, self.dict2int( { 'addr':5 , 'frac_lsb_set':0 , 'frac_sd':frac_sd , }))

        self.wr_chronos(  6, self.dict2int( { 'addr':6 , 'spare_out':0 , 'dummy_dis':0 , 'out_pwr':1 , 'pga_gain':1 , 'pwr_alm_level':0 , 'en_chp_ldo':1 , 'testmux(6:5)':0 , 'sft_rst_tgl':0 , 'dis_d':1 , 'nbits_d':0 , }))

        self.wr_chronos(  7, self.dict2int( { 'addr':7 , 'set_outvrnt':0 , 'dis_itprot':1 , 'ref_freq_stm':2 , 'axc_tgl':0 , 'retry_stm':0 , 'atc_or':0 , 'alc_or':0 , 'atc(5:0)':0 , 'alc':0 , }))

        self.wr_chronos(  8, self.dict2int( { 'addr':8 , 'en_amux':0 , 'sel_amux':0 , 'en_vtune':0 , 'set_leak_chp':0 , 'ld_en':1 , 'mux_ctrl_ld':0 , 'chp_set_tune':2 , 'ichp_set(1:0)':1 , 'chp_source':0 , 'chp_sink':0 , 'chp_test_en':0 , }))

        self.wr_chronos(  9, self.dict2int( { 'addr':9 , 'en_pfd':1 , 'en_iset_bias':0 , 'iset_bias':0 , 'spi_ld_stm_sel':0 , 'aut_outamp':0 , 'en_x2_outamp':en_x2_outamp , 'en_divn':1 , 'en_outamp':1 , 'vco_en':1 , 'atc(6)':1 , 'ichp_set(2)':0 , }))

        self.wr_chronos( 10, self.dict2int( { 'addr':10 , 'en_pwr_alm':0 , 'chp_delay':0 , 'thr_alccomp':7 , 'en_axctest':0 , 'vlo_atccomp':5 , 'vhi_atccomp':10 , }))

        # Toggle axc_tgl (it will reset itself)
        self.wr_chronos(  7, self.dict2int( { 'addr':7 , 'set_outvrnt':0 , 'dis_itprot':1 , 'ref_freq_stm':2 , 'axc_tgl':1 , 'retry_stm':0 , 'atc_or':0 , 'alc_or':0 , 'atc(5:0)':0 , 'alc':0 , }))

        import time
        time.sleep( 0.2) # wait for Chronos to stabilize
        aa1 = self.rd_chronos( 'reg_00')
        if not ( self.rd_chronos( 'reg_00')[ 'dict'][ 'res_crs']):
            print('RES_CRS is 0, setting ATC(6) to 0')

            self.wr_chronos( 9, self.dict2int( { 'addr':9 , 'en_pfd':1 , 'en_iset_bias':0 , 'iset_bias':0 , 'spi_ld_stm_sel':0 , 'aut_outamp':0 , 'en_x2_outamp':en_x2_outamp , 'en_divn':1 , 'en_outamp':1 , 'vco_en':1 , 'atc(6)':0 , 'ichp_set(2)':0 , }))

            # Toggle axc_tgl again
            self.wr_chronos( 7, self.dict2int( { 'addr':7 , 'set_outvrnt':0 , 'dis_itprot':1 , 'ref_freq_stm':2 , 'axc_tgl':1 , 'retry_stm':0 , 'atc_or':0 , 'alc_or':0 , 'atc(5:0)':0 , 'alc':0 , }))        
        time.sleep( 0.2) # wait for Chronos to stabilize
        if not int_mode:
            self.wr_chronos(  4, self.dict2int( { 'addr':4 , 'order_sd':3 , 'nint_sd':nint_sd , }))


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
        
    def setAWVRX(self, index, awv):
        if index > 63 or index<0:
            success = False
            status = 'ERROR: RX beam index should be between 0 and 63'
            return success, status
        elif len(awv) != 32:
            success = False
            status = 'ERROR: The length of AWV should be 32'
            return success, status
        else:
            address, size = self.getAddressAndSize('bf_rx_awv')  
            data = awv
            address = int(address) + index*32
            print(hex(address))
            command = int2intlist((address << 3) + self.SPI_WR_RAW,256,2)
            data.append(0)
            self.spiSiver.write(command+data,start=True, stop=True)   
            success = True
            status = 'Success'             
            return success, status    
        
    def getAWVRX(self, index):
        if index > 63 or index<0:
            success = False
            status = 'ERROR: RX beam index should be between 0 and 63'
            return status
        else:
            address, size = self.getAddressAndSize('bf_rx_awv')  
            address = int(address) + index*32
            size = 32;
            command  = int2intlist((address << 3) + self.SPI_RD,256,2)
            read_buf = self.spiSiver.exchange(command,2+size,start=True, stop=True, duplex=True)
            read_buf = read_buf[2:]
            return (list(read_buf))
        
    def getAWVTX(self, index):
        if index > 63 or index<0:
            success = False
            status = 'ERROR: TX beam index should be between 0 and 63'
            print(status)
            return status
        else:
            address, size = self.getAddressAndSize('bf_tx_awv')  
            address = int(address) + index*32
            size = 32;
            command  = int2intlist((address << 3) + self.SPI_RD,256,2)
            read_buf = self.spiSiver.exchange(command,2+size,start=True, stop=True, duplex=True)
            read_buf = read_buf[2:]
            return (list(read_buf))    
        
    def setAWVTX(self, index, awv):
        if index > 63 or index<0:
            success = False
            status = 'ERROR: TX beam index should be between 0 and 63'
            print(status)
            return success, status
        elif len(awv) != 32:
            success = False
            status = 'ERROR: The length of AWV should be 32'
            print(status)
            return success, status
        else:
            address, size = self.getAddressAndSize('bf_tx_awv')  
            data = awv
            address = int(address) + index*32
            print(hex(address))
            command = int2intlist((address << 3) + self.SPI_WR_RAW,256,2)
            data.append(0)
            self.spiSiver.write(command+data,start=True, stop=True)   
            success = True
            status = 'Success'    
            print(status)
            return success, status          

    def getBeamIndexTX(self):
        return 0x7F & self.rd('bf_tx_awv_ptr')

    def getBeamIndexRX(self):
        return 0x7F & self.rd('bf_rx_awv_ptr')
  

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
            
            
    # Chronos
   # print a placeholder for field values according to an address.
    # Actual values can be filled into the placeholder and then it can
    # be used as argument for dict2int() as argument for chronos.wr()
    def printfmt( self, reg_name):
        bsize = None
        address,bsize = self.get_addr_and_size( reg_name, bsize)
        fmt_str = "{ "
        for k, v in list(self.reg_fmt[ address].items()):
            if not 'unused' in k:
                if k == 'addr':
                    def_val = address
                else:
                    def_val = 0
                    
                fmt_str += "'%s':%d , " % ( k, def_val)

        fmt_str += "}"

        return fmt_str

    # def printfmt

    
    # convert a dictionary of values into 24-bit integer using
    # a format specified by din['addr']
    def dict2int( self, din):
        val_binstr = ''
        for k, v in list(self.reg_fmt[ din[ 'addr']].items()):
            if 'unused' in k:
                tmp_val = 0
            else:
                tmp_val = din[ k]

            val_binstr += format( tmp_val, '0%db' % v)

        return int( val_binstr, 2)
    
    # def dict2int    
    
    def addr(self, reg_name):
        """Return decimal address for symbolic address"""
        return self.regs_chronos[reg_name]['addr']

    def size(self, reg_name):
        """Return size of symbolic address"""
        return self.regs_chronos[reg_name]['size']

    def get_addr_and_size(self, reg_name, bsize):
        if isinstance(reg_name,int):
            address = reg_name
            if bsize is None:
                for key,reg in self.regs_chronos.items():
                    if reg['addr'] == reg_name:
                        bsize = self.size(key)
        else:
            address = self.addr(reg_name)
            if bsize is None:
                bsize = self.size(reg_name)
        return address,bsize    
    
    def wr_chronos(self, reg_name, data, bsize=None, debug=0):
        """Write new contents to register 'addr'.
           Register name or address can be given as memory destination.
           Example: wr('reg_03',0x310203)
                    wr(0x3, 0x310203)
        """
        self.gpioC.write(0x00) # select chronos

        address,bsize = self.get_addr_and_size( reg_name, bsize)
        assert( bsize == 3)
        assert( type( data) is int)

        data = int2intlist( data, 256, bsize) + int2intlist( 0x00, 256, 1)
        assert( ( data[ 0] >> 4) == address)
        
        #data.append(0)
        self.spiChronos.write(data,start=True, stop=True) ## not sure if this is correct.
        self.gpioC.write(0xFF) # select Cruijff
        return 0    
    
    
    def rd_chronos( self, reg_name, bsize=None, lst=0, debug=0):
        """Read contents of register 'addr' and return as integer and
           as a dictionary of field:value pairs
           Example: rd('reg_00')
        """
        self.gpioC.write(0x00) # select chronos
        address,bsize = self.get_addr_and_size( reg_name, bsize)
        assert( bsize == 3)
        
        data = bsize * [0x00]
        data[ 0] |= address << 4
        
        if debug:
            print(data)

        ret_dict = {}
        answer = 1
        try:
            #rdval = self.evkplatform.spi_xfer( data)
            rdval = self.spiChronos.exchange(data,bsize,start=True, stop=True, duplex=True)
            rdval = rdval[0:]            
            
        except:
            print(' Chronos SPI read error.')
            answer = 0

        if answer:
            rdval_int = intlist2int( rdval)

            if debug: 
                print(hex( rdval_int))

            # parse according to format using the address
            rdval_binstr = format( rdval_int, "024b")
            pos = 0

            for k, v in list(self.reg_fmt[ address].items()):
                tmp_val = int( rdval_binstr[ pos : pos + v], 2)
                if k == 'addr' and address != tmp_val:
                    print(( 'Chronos SPI read error: requested address is 0x%x ' + \
                           'but actual address is 0x%x. Is Chronos chip selected?') % \
                           ( address, tmp_val))
                    break

                if not 'unused' in k:
                    if debug:
                        print(( '%s = %d') % ( k, tmp_val))

                    ret_dict[ k] = tmp_val
                    
                pos += v
            
            if lst:
                num_ints = int(ceil(bsize/lst))
                answer = intlist2intlist( rdval, 256**lst, num_ints, 256)
            else:
                answer = intlist2int( rdval)

        self.gpioC.write(0xFF) # select Cruijff
        return { 'int': answer, 'dict' : ret_dict}
    