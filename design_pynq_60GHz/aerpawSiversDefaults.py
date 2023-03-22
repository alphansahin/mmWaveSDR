import aerpawSiversDoc as doc

class siversDefaults():
    def __init__(self):
       
        self.freq = 45e6               # XO reference frequency
        self.freq_alt = 40e6           # Alternative XO reference frequency
        self.freq_sel_limit = (self.freq + self.freq_alt)/2       
        self.chipType = 'Eder B MMF'
        self.rfmType = 'BFM06010'


        if self.chipType == 'Eder B MMF':
            #ADC reference measured for 12 units at T = 0 degrees,
            #Use 1.217 for other voltage measurements (found at T = 25 degrees)
            self.adc_ref_volt = 1.213                                    # [V]
            self.temp_k       = 3.6805e-3                                # [V/K]
            self.temp_offs    = 0.2052                                   # [1/V]
        else: # Eder B
            self.adc_ref_volt = 1.228                                    # [V]
            self.temp_k       = 4e-3                                     # [V/K]
            self.temp_offs    = 41e-3                                    # [K/V]
        
        self.adc_max      = 4095
        self.adc_scale    = 3
        self.unit_offs    = {'K':0, 'C':-273}        
        self.temp_scale   = self.adc_scale*self.adc_ref_volt/self.adc_max/self.temp_k    # [K]
        self.temp_comp    = self.temp_offs/self.temp_k                         # [K]
        self.temp_calib_offset = 0

        self.alc_th_v=1.244              # VCO amplitude threshold = 1.196 V @ 25 degC
        self.atc_hi_th_v=2.4             # High tune voltage threshold = 2.4V
        self.atc_lo_th_v=0.4             # Low tune voltage threshold = 0.4V
        self.alc_th=102
        #self.atc_hi_th=191
        self.atc_lo_th=34
        self.dac_ref=2.8                 #Changed from 3.0 to 2.8 in Rev. B MMF
        self.a_freq=0
        self.vtune=0
        self.vtune_th=0
        self.t=-273
        self.adc_ref_volt = 1.1
        #self.adc_max      = 4095
        #self.adc_scale    = 3
        self.adc_num_samp = 256
        self.temp_k       = 4e-3
        self.alc_path = '/lut/vco'

        self.fc = 60.48e9
        self.bias_vco_x3_lo_freq = 61.29e9
        self.bias_vco_x3_hi_freq = 68.31e9        

        # DC sense calibration
        self.amux_dc_sense_calib = 0x40

        # bist_amux_ctrl
        # ==============
        self.amux_bg_pll       = 0
        self.amux_bg_tx        = 1
        self.amux_bg_rx        = 2
        self.amux_temp         = 3
        self.amux_rx_bb        = 4
        self.amux_vco          = 5
        self.amux_vcc_pll      = 6
        self.amux_tx_pdet      = 7
        self.amux_adc_ref      = 8
        self.amux_dco_i        = 9
        self.amux_dco_q        = 10
        self.amux_dco_cm       = 11
        self.amux_otp          = 12
        self.amux_tx_env_pdet  = 13
        self.amux_vcc_pa       = 14
        self.amux_vcc_tx       = 15

        # amux_rx_bb (rx_bb_test_ctrl)
        # ============================
        self.rx_bb_mix_pd_i    = 1
        self.rx_bb_mix_pd_q    = 2
        self.rx_bb_mix_pd_th_i = 5
        self.rx_bb_mix_pd_th_q = 6
        self.rx_bb_mix_dc_p_i  = 9
        self.rx_bb_mix_dc_p_q  = 10
        self.rx_bb_mix_dc_n_i  = 13
        self.rx_bb_mix_dc_n_q  = 14
        self.rx_bb_inb_pd_i    = 17
        self.rx_bb_inb_pd_q    = 18
        self.rx_bb_inb_pd_th_i = 21
        self.rx_bb_inb_pd_th_q = 22
        self.rx_bb_inb_dc_p_i  = 25
        self.rx_bb_inb_dc_p_q  = 26
        self.rx_bb_inb_dc_n_i  = 29
        self.rx_bb_inb_dc_n_q  = 30
        self.rx_bb_vga1_pd_i    = 33
        self.rx_bb_vga1_pd_q    = 34
        self.rx_bb_vga1_pd_th_i = 37
        self.rx_bb_vga1_pd_th_q = 38
        self.rx_bb_vga1_dc_p_i  = 41
        self.rx_bb_vga1_dc_p_q  = 42
        self.rx_bb_vga1_dc_n_i  = 45
        self.rx_bb_vga1_dc_n_q  = 46
        self.rx_bb_vga2_pd_i    = 49
        self.rx_bb_vga2_pd_q    = 50
        self.rx_bb_vga2_pd_th_i = 53
        self.rx_bb_vga2_pd_th_q = 54
        self.rx_bb_vga2_dc_p_i  = 57
        self.rx_bb_vga2_dc_p_q  = 58
        self.rx_bb_vga2_dc_n_i  = 61
        self.rx_bb_vga2_dc_n_q  = 62
        self.rx_bb_vga1db_pd_i    = 65
        self.rx_bb_vga1db_pd_q    = 66
        self.rx_bb_vga1db_pd_th_i = 69
        self.rx_bb_vga1db_pd_th_q = 70
        self.rx_bb_vga1db_dc_p_i  = 73
        self.rx_bb_vga1db_dc_p_q  = 74
        self.rx_bb_vga1db_dc_n_i  = 77
        self.rx_bb_vga1db_dc_n_q  = 78
        self.rx_bb_outb_pd_i    = 81
        self.rx_bb_outb_pd_q    = 82
        self.rx_bb_outb_pd_th_i = 85
        self.rx_bb_outb_pd_th_q = 86
        self.rx_bb_outb_dc_p_i  = 89
        self.rx_bb_outb_dc_p_q  = 90
        self.rx_bb_outb_dc_n_i  = 93
        self.rx_bb_outb_dc_n_q  = 94

        # vco_amux_ctrl
        # =============
        self.vco_alc_th    = 0
        self.vco_vco_amp   = 1
        self.vco_atc_lo_th = 2
        self.vco_atc_hi_th = 3
        self.vco_vcc_vco   = 4
        self.vco_vcc_chp   = 5
        self.vco_vcc_synth = 6
        self.vco_vcc_bb_tx = 7
        self.vco_vcc_bb_rx = 8

        # bist_otp_ctrl
        # =============
        self.otp_temp_th   = 0
        self.otp_vdd_1v2   = 1
        self.otp_vdd_1v8   = 2
        self.otp_vcc_rx    = 3

        # pll_ld_mux_ctrl
        # ===============
        self.pll_ld_ld     = 0
        self.pll_ld_xor    = 1
        self.pll_ld_ref    = 2
        self.pll_ld_vco    = 3
        self.pll_ld_ld_raw = 4
        self.pll_ld_tst_0  = 5
        self.pll_ld_tst_1  = 6

        # amux_tx_env_pdet (tx_bf_pdet_mux)
        # =================================
        self.pdet          = (0 << 4)
        self.alc_lo_th     = (1 << 4)
        self.alc_hi_th     = (2 << 4)
        self.dig_pll_vtune = (3 << 4)


        self.SPI_WR_RAW  = 0
        self.SPI_WR_CLR  = 1
        self.SPI_WR_NAND = 1
        self.SPI_WR_SET  = 2
        self.SPI_WR_OR   = 2
        self.SPI_WR_TGL  = 3
        self.SPI_WR_XOR  = 3
        self.SPI_RD      = 4

        self.RX_MODE   = 0
        self.TX_MODE   = 1
        self.TXRX_MODE = 2        
        
        self.regs =   {'chip_id':      {'group':'system', 'addr':0x0000, 'size':4, 'value':0x02731803, 'mask':0xFFFFFFFF, 'doc':doc.chip_id_help},
            'chip_id_sw_en':           {'group':'system', 'addr':0x0004, 'size':1, 'value':0x00, 'mask':0x01, 'doc':doc.chip_id_sw_en_help},
            'fast_clk_ctrl':           {'group':'system', 'addr':0x0005, 'size':1, 'value':0x00, 'mask':0x33, 'doc':doc.fast_clk_ctrl_help},
            'gpio_tx_rx_sw_ctrl':      {'group':'system', 'addr':0x0006, 'size':1, 'value':0x00, 'mask':0x13, 'doc':doc.gpio_tx_rx_sw_ctrl_help},
            'gpio_agc_rst_ctrl':       {'group':'system', 'addr':0x0007, 'size':1, 'value':0x00, 'mask':0x13, 'doc':doc.gpio_agc_rst_ctrl_help},
            'gpio_agc_start_ctrl':     {'group':'system', 'addr':0x0008, 'size':1, 'value':0x00, 'mask':0x13, 'doc':doc.gpio_agc_start_ctrl_help},
            'gpio_agc_gain_in_ctrl':   {'group':'system', 'addr':0x0009, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.gpio_agc_gain_in_ctrl_help},
            'gpio_agc_gain_out_ctrl':  {'group':'system', 'addr':0x000a, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.gpio_agc_gain_out_ctrl_help},
            'bist_amux_ctrl':          {'group':'system', 'addr':0x000b, 'size':1, 'value':0x00, 'mask':0xCF, 'doc':doc.bist_amux_ctrl_help},
            'bist_ot_ctrl':            {'group':'system', 'addr':0x000d, 'size':1, 'value':0x00, 'mask':0x33, 'doc':doc.bist_ot_ctrl_help},
            'bist_ot_temp':            {'group':'system', 'addr':0x000e, 'size':1, 'value':0x80, 'mask':0xDF, 'doc':doc.bist_ot_temp_help},
            'bist_ot_rx_off_mask':     {'group':'system', 'addr':0x000f, 'size':3, 'value':0x000000, 'mask':0x1FFFFF, 'doc':doc.bist_ot_rx_off_mask_help},
            'bist_ot_tx_off_mask':     {'group':'system', 'addr':0x0012, 'size':3, 'value':0x000000, 'mask':0x1FFFFF, 'doc':doc.bist_ot_tx_off_mask_help},
            'spare':                   {'group':'system', 'addr':0x001C, 'size':4, 'value':0xFF0000FF, 'mask':0xFFFFFFFF, 'doc':doc.spare_help},
            #
            'bias_ctrl':               {'group':'bias',   'addr':0x0020, 'size':1, 'value':0x00, 'mask':0x7F, 'doc':doc.bias_ctrl_help},
            'bias_vco_x3':             {'group':'bias',   'addr':0x0021, 'size':1, 'value':0x00, 'mask':0x03, 'doc':doc.bias_vco_x3_help},
            'bias_pll':                {'group':'bias',   'addr':0x0022, 'size':1, 'value':0x00, 'mask':0x37, 'doc':doc.bias_pll_help},
            'bias_lo':                 {'group':'bias',   'addr':0x0023, 'size':1, 'value':0x00, 'mask':0x3F, 'doc':doc.bias_lo_help},
            'bias_tx':                 {'group':'bias',   'addr':0x0024, 'size':2, 'value':0x0000, 'mask':0xFFFF, 'doc':doc.bias_tx_help},
            'bias_rx':                 {'group':'bias',   'addr':0x0026, 'size':2, 'value':0x0000, 'mask':0x0FFF, 'doc':doc.bias_rx_help},
            #
            'pll_en':                  {'group':'pll',    'addr':0x0040, 'size':1, 'value':0x00, 'mask':0x7F, 'doc':doc.pll_en_help},
            'pll_divn':                {'group':'pll',    'addr':0x0041, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.pll_divn_help},
            'pll_pfd':                 {'group':'pll',    'addr':0x0042, 'size':1, 'value':0x00, 'mask':0x07, 'doc':doc.pll_pfd_help},
            'pll_chp':                 {'group':'pll',    'addr':0x0043, 'size':1, 'value':0x00, 'mask':0x73, 'doc':doc.pll_chp_help},
            'pll_ld_mux_ctrl':         {'group':'pll',    'addr':0x0044, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.pll_ld_mux_ctrl_help},
            'pll_test_mux_in':         {'group':'pll',    'addr':0x0045, 'size':1, 'value':0x00, 'mask':0x03, 'doc':doc.pll_test_mux_in_help},
            'pll_ref_in_lvds_en':      {'group':'pll',    'addr':0x0046, 'size':1, 'value':0x00, 'mask':0x03, 'doc':doc.pll_ref_in_lvds_en_help},
            #
            'tx_ctrl':                 {'group':'tx',     'addr':0x0060, 'size':1, 'value':0x10, 'mask':0x7F, 'doc':doc.tx_ctrl_help},
            'tx_bb_q_dco':             {'group':'tx',     'addr':0x0061, 'size':1, 'value':0x40, 'mask':0x7F, 'doc':doc.tx_bb_q_dco_help},
            'tx_bb_i_dco':             {'group':'tx',     'addr':0x0062, 'size':1, 'value':0x40, 'mask':0x7F, 'doc':doc.tx_bb_i_dco_help},
            'tx_bb_phase':             {'group':'tx',     'addr':0x0063, 'size':1, 'value':0x00, 'mask':0x1F, 'doc':doc.tx_bb_phase_help},
            'tx_bb_gain':              {'group':'tx',     'addr':0x0064, 'size':1, 'value':0x00, 'mask':0x23, 'doc':doc.tx_bb_gain_help},
            'tx_bb_iq_gain':           {'group':'tx',     'addr':0x0065, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.tx_bb_iq_gain_help},
            'tx_bfrf_gain':            {'group':'tx',     'addr':0x0066, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.tx_bfrf_gain_help},
            'tx_bf_pdet_mux':          {'group':'tx',     'addr':0x0067, 'size':1, 'value':0x00, 'mask':0xBF, 'doc':doc.tx_bf_pdet_mux_help},
            'tx_alc_ctrl':             {'group':'tx',     'addr':0x0068, 'size':1, 'value':0x00, 'mask':0xF3, 'doc':doc.tx_alc_ctrl_help},
            'tx_alc_loop_cnt':         {'group':'tx',     'addr':0x0069, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.tx_alc_loop_cnt_help},
            'tx_alc_start_delay':      {'group':'tx',     'addr':0x006A, 'size':2, 'value':0x0000, 'mask':0xFFFF, 'doc':doc.tx_alc_start_delay_help},
            'tx_alc_meas_delay':       {'group':'tx',     'addr':0x006C, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.tx_alc_meas_delay_help},
            'tx_alc_bfrf_gain_max':    {'group':'tx',     'addr':0x006D, 'size':1, 'value':0xFF, 'mask':0xFF, 'doc':doc.tx_alc_bfrf_gain_max_help},
            'tx_alc_bfrf_gain_min':    {'group':'tx',     'addr':0x006E, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.tx_alc_bfrf_gain_min_help},
            'tx_alc_step_max':         {'group':'tx',     'addr':0x006F, 'size':1, 'value':0x00, 'mask':0x33, 'doc':doc.tx_alc_step_max_help},
            'tx_alc_pdet_lo_th':       {'group':'tx',     'addr':0x0070, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.tx_alc_pdet_lo_th_help},
            'tx_alc_pdet_hi_offs_th':  {'group':'tx',     'addr':0x0071, 'size':1, 'value':0x00, 'mask':0x1F, 'doc':doc.tx_alc_pdet_hi_offs_th_help},
            'tx_alc_bfrf_gain':        {'group':'tx',     'addr':0x0072, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.tx_alc_bfrf_gain_help},
            'tx_alc_pdet':             {'group':'tx',     'addr':0x0073, 'size':1, 'value':0x00, 'mask':0x03, 'doc':doc.tx_alc_pdet_help},
            #
            'adc_ctrl':                {'group':'adc',    'addr':0x0080, 'size':1, 'value':0x00, 'mask':0xB7, 'doc':doc.adc_ctrl_help},
            'adc_clk_div':             {'group':'adc',    'addr':0x0081, 'size':1, 'value':0x03, 'mask':0xFF, 'doc':doc.adc_clk_div_help},
            'adc_sample_cycle':        {'group':'adc',    'addr':0x0082, 'size':1, 'value':0x00, 'mask':0x3F, 'doc':doc.adc_sample_cycle_help},
            'adc_num_samples':         {'group':'adc',    'addr':0x0083, 'size':1, 'value':0x00, 'mask':0x0F, 'doc':doc.adc_num_samples_help}, 
            'adc_sample':              {'group':'adc',    'addr':0x0090, 'size':2, 'value':0x000, 'mask':0x0FFF, 'doc':doc.adc_sample_help},
            'adc_mean':                {'group':'adc',    'addr':0x0092, 'size':2, 'value':0x000, 'mask':0x0FFF, 'doc':doc.adc_mean_help},
            'adc_max':                 {'group':'adc',    'addr':0x0094, 'size':2, 'value':0x000, 'mask':0x0FFF, 'doc':doc.adc_max_help},
            'adc_min':                 {'group':'adc',    'addr':0x0096, 'size':2, 'value':0x000, 'mask':0x0FFF, 'doc':doc.adc_min_help},
            'adc_diff':                {'group':'adc',    'addr':0x0098, 'size':2, 'value':0x0000, 'mask':0x1FFF, 'doc':doc.adc_diff_help},
            #
            'vco_en':                  {'group':'vco',    'addr':0x00A0, 'size':1, 'value':0x00, 'mask':0x7F, 'doc':doc.vco_en_help},
            'vco_dig_tune':            {'group':'vco',    'addr':0x00A1, 'size':1, 'value':0x00, 'mask':0x7F, 'doc':doc.vco_dig_tune_help},
            'vco_ibias':               {'group':'vco',    'addr':0x00A2, 'size':1, 'value':0x00, 'mask':0x3F, 'doc':doc.vco_ibias_help},
            'vco_vtune_ctrl':          {'group':'vco',    'addr':0x00A3, 'size':1, 'value':0x00, 'mask':0x33, 'doc':doc.vco_vtune_ctrl_help},
            'vco_vtune_atc_lo_th':     {'group':'vco',    'addr':0x00A4, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_vtune_atc_lo_th_help},
            'vco_amux_ctrl':           {'group':'vco',    'addr':0x00A5, 'size':1, 'value':0x00, 'mask':0x1F, 'doc':doc.vco_amux_ctrl_help},
            'vco_vtune_th':            {'group':'vco',    'addr':0x00A6, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_vtune_th_help},
            'vco_atc_hi_th':           {'group':'vco',    'addr':0x00A7, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_atc_hi_th_help},
            'vco_atc_lo_th':           {'group':'vco',    'addr':0x00A8, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_atc_lo_th_help},
            'vco_alc_hi_th':           {'group':'vco',    'addr':0x00A9, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_alc_hi_th_help},
            'vco_override_ctrl':       {'group':'vco',    'addr':0x00AA, 'size':2, 'value':0x00, 'mask':0x01FF, 'doc':doc.vco_override_ctrl_help},
            'vco_alc_del':             {'group':'vco',    'addr':0x00AC, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_alc_del_help},
            'vco_vtune_del':           {'group':'vco',    'addr':0x00AD, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_vtune_del_help},
            'vco_tune_loop_del':       {'group':'vco',    'addr':0x00AE, 'size':3, 'value':0x00, 'mask':0x03FFFF, 'doc':doc.vco_tune_loop_del_help},
            'vco_atc_vtune_set_del':   {'group':'vco',    'addr':0x00B1, 'size':3, 'value':0x00, 'mask':0x03FFFF, 'doc':doc.vco_atc_vtune_set_del_help},
            'vco_atc_vtune_unset_del': {'group':'vco',    'addr':0x00B4, 'size':3, 'value':0x00, 'mask':0x03FFFF, 'doc':doc.vco_atc_vtune_unset_del_help},
            'vco_tune_ctrl':           {'group':'vco',    'addr':0x00B7, 'size':1, 'value':0x00, 'mask':0x77, 'doc':doc.vco_tune_ctrl_help},
            'vco_tune_status':         {'group':'vco',    'addr':0x00B8, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.vco_tune_status_help},
            'vco_tune_det_status':     {'group':'vco',    'addr':0x00B9, 'size':1, 'value':0x00, 'mask':0x0F, 'doc':doc.vco_tune_det_status_help},
            'vco_tune_freq_cnt':       {'group':'vco',    'addr':0x00BA, 'size':2, 'value':0x000, 'mask':0x0FFF, 'doc':doc.vco_tune_freq_cnt_help},
            'vco_tune_dig_tune':       {'group':'vco',    'addr':0x00BC, 'size':1, 'value':0x40, 'mask':0x7F, 'doc':doc.vco_tune_dig_tune_help},
            'vco_tune_ibias':          {'group':'vco',    'addr':0x00BD, 'size':1, 'value':0x00, 'mask':0x3F, 'doc':doc.vco_tune_ibias_help},
            'vco_tune_vtune':          {'group':'vco',    'addr':0x00BE, 'size':1, 'value':0x80, 'mask':0xFF, 'doc':doc.vco_tune_vtune_help},
            'vco_tune_fd_polarity':    {'group':'vco',    'addr':0x00BF, 'size':1, 'value':0x01, 'mask':0x01, 'doc':doc.vco_tune_fd_polarity_help},
            #
            'rx_gain_ctrl_mode':       {'group':'rx',     'addr':0x00C0, 'size':1, 'value':0x00, 'mask':0x3B, 'doc':doc.rx_gain_ctrl_mode_help},
            'rx_gain_ctrl_reg_index':  {'group':'rx',     'addr':0x00C1, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.rx_gain_ctrl_reg_index_help},
            'rx_gain_ctrl_sel':        {'group':'rx',     'addr':0x00C2, 'size':2, 'value':0x0000, 'mask':0x03FF, 'doc':doc.rx_gain_ctrl_sel_help},
            'rx_gain_ctrl_bfrf':       {'group':'rx',     'addr':0x00C4, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.rx_gain_ctrl_bfrf_help},
            'rx_gain_ctrl_bb1':        {'group':'rx',     'addr':0x00C5, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.rx_gain_ctrl_bb1_help},
            'rx_gain_ctrl_bb2':        {'group':'rx',     'addr':0x00C6, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.rx_gain_ctrl_bb2_help},
            'rx_gain_ctrl_bb3':        {'group':'rx',     'addr':0x00C7, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.rx_gain_ctrl_bb3_help},
            'rx_bb_q_dco':             {'group':'rx',     'addr':0x00C8, 'size':2, 'value':0x40, 'mask':0x3FFF, 'doc':doc.rx_bb_q_dco_help},
            'rx_bb_i_dco':             {'group':'rx',     'addr':0x00CA, 'size':2, 'value':0x40, 'mask':0x3FFF, 'doc':doc.rx_bb_i_dco_help},
            'rx_dco_en':               {'group':'rx',     'addr':0x00CC, 'size':1, 'value':0x00, 'mask':0x01, 'doc':doc.rx_dco_en_help},
            'rx_drv_dco':              {'group':'rx',     'addr':0x001C, 'size':4, 'value':0xFF0000FF, 'mask':0xFFFFFFFF, 'doc':doc.rx_drv_dco_help},
            'rx_bb_biastrim':          {'group':'rx',     'addr':0x00CD, 'size':1, 'value':0x00, 'mask':0x3F, 'doc':doc.rx_bb_biastrim_help},
            'rx_bb_test_ctrl':         {'group':'rx',     'addr':0x00CE, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.rx_bb_test_ctrl_help},
            #
            'agc_int_ctrl':            {'group':'agc',    'addr':0x00E0, 'size':1, 'value':0x00, 'mask':0x03, 'doc':doc.agc_int_ctrl_help},
            'agc_int_en_ctrl':         {'group':'agc',    'addr':0x00E1, 'size':1, 'value':0x20, 'mask':0x1F, 'doc':doc.agc_int_en_ctrl_help},
            'agc_int_backoff':         {'group':'agc',    'addr':0x00E2, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.agc_int_backoff_help},
            'agc_int_start_del':       {'group':'agc',    'addr':0x00E3, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.agc_int_start_del_help},
            'agc_int_timeout':         {'group':'agc',    'addr':0x00E4, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.agc_int_timeout_help},
            'agc_int_gain_change_del': {'group':'agc',    'addr':0x00E5, 'size':1, 'value':0x05, 'mask':0x0F, 'doc':doc.agc_int_gain_change_del_help},
            'agc_int_pdet_en':         {'group':'agc',    'addr':0x00E6, 'size':1, 'value':0x09, 'mask':0x0F, 'doc':doc.agc_int_pdet_en_help},
            'agc_int_pdet_filt':       {'group':'agc',    'addr':0x00E7, 'size':2, 'value':0x1F1F, 'mask':0x1FFF, 'doc':doc.agc_int_pdet_filt_help},
            'agc_int_pdet_th':         {'group':'agc',    'addr':0x00E9, 'size':5, 'value':0x0000000000, 'mask':0xFFFFFFFFFF, 'doc':doc.agc_int_pdet_th_help},
            'agc_int_bfrf_gain_lvl':   {'group':'agc',    'addr':0x00EE, 'size':4, 'value':0xFFCC9966, 'mask':0xFFFFFFFF, 'doc':doc.agc_int_bfrf_gain_lvl_help},
            'agc_int_bb3_gain_lvl':    {'group':'agc',    'addr':0x00F2, 'size':3, 'value':0xFCA752, 'mask':0xFFFFFF, 'doc':doc.agc_int_bb3_gain_lvl_help},
            'agc_int_status_pdet':     {'group':'agc',    'addr':0x00F5, 'size':2, 'value':0xF4, 'mask':0x1FFF, 'doc':doc.agc_int_status_pdet_help},
            'agc_int_status':          {'group':'agc',    'addr':0x00F7, 'size':1, 'value':0x00, 'mask':0x03, 'doc':doc.agc_int_status_help},
            'agc_int_gain':            {'group':'agc',    'addr':0x00F8, 'size':1, 'value':0x00, 'mask':0xFF, 'doc':doc.agc_int_gain_help},
            'agc_int_gain_setting':    {'group':'agc',    'addr':0x00F9, 'size':4, 'value':0xFFFFFFFF, 'mask':0xFFFFFFFF, 'doc':doc.agc_int_gain_setting_help},
            'agc_ext_ctrl':            {'group':'agc',    'addr':0x00FD, 'size':1, 'value':0x05, 'mask':0x07, 'doc':doc.agc_ext_ctrl_help},

            #
            'trx_ctrl':                {'group':'trx',    'addr':0x01C0, 'size':1, 'value':0x00, 'mask':0x3B, 'doc':doc.trx_ctrl_help},
            'trx_soft_ctrl':           {'group':'trx',    'addr':0x01C1, 'size':1, 'value':0x00, 'mask':0x03, 'doc':doc.trx_soft_ctrl_help},
            'trx_soft_delay':          {'group':'trx',    'addr':0x01C2, 'size':1, 'value':0x00, 'mask':0x07, 'doc':doc.trx_soft_delay_help},
            'trx_soft_max_state':      {'group':'trx',    'addr':0x01C3, 'size':1, 'value':0x00, 'mask':0x07, 'doc':doc.trx_soft_max_state_help},
            'trx_tx_on':               {'group':'trx',    'addr':0x01C4, 'size':3, 'value':0x1FFFFF, 'mask':0x1FFFFF, 'doc':doc.trx_tx_on_help},
            'trx_tx_off':              {'group':'trx',    'addr':0x01C7, 'size':3, 'value':0x00, 'mask':0x1FFFFF, 'doc':doc.trx_tx_off_help},
            'trx_rx_on':               {'group':'trx',    'addr':0x01CA, 'size':3, 'value':0x1FFFFF, 'mask':0x1FFFFF, 'doc':doc.trx_rx_on_help},
            'trx_rx_off':              {'group':'trx',    'addr':0x01CD, 'size':3, 'value':0x00, 'mask':0x1FFFFF, 'doc':doc.trx_rx_off_help},
            'trx_soft_tx_on_enables':  {'group':'trx',    'addr':0x01E0, 'size':8, 'value':0x00, 'mask':0x1F1F1F1F1F1F1F1F, 'doc':doc.trx_soft_tx_on_enables_help},
            'trx_soft_rx_on_enables':  {'group':'trx',    'addr':0x01E8, 'size':8, 'value':0x00, 'mask':0x1F1F1F1F1F1F1F1F, 'doc':doc.trx_soft_rx_on_enables_help},
            'trx_soft_bf_on_grp_sel':  {'group':'trx',    'addr':0x01F0, 'size':4, 'value':0x00, 'mask':0xFFFFFFFF, 'doc':doc.trx_soft_bf_on_grp_sel_help},
       
            'bf_tx_awv_idx_table':   {'group':'bf_tx', 'addr':0x0100, 'size':64, 'value':0x00},
            'bf_tx_awv_idx':         {'group':'bf_tx', 'addr':0x0140, 'size':1,  'value':0x00},
            'bf_tx_awv_ce':          {'group':'bf_tx', 'addr':0x0141, 'size':1,  'value':0x00},
            'bf_tx_cfg':             {'group':'bf_tx', 'addr':0x0143, 'size':1,  'value':0x01},
            #
            'bf_rx_awv_idx_table':   {'group':'bf_rx', 'addr':0x0160, 'size':64, 'value':0x00},
            'bf_rx_awv_idx':         {'group':'bf_rx', 'addr':0x01A0, 'size':1,  'value':0x00},
            'bf_rx_awv_ce':          {'group':'bf_rx', 'addr':0x01A1, 'size':1,  'value':0x00},
            'bf_rx_cfg':             {'group':'bf_rx', 'addr':0x01A3, 'size':1,  'value':0x01},

            'bf_tx_mbist_0_pat':     {'group':'bf_tx', 'addr':0x0144, 'size':2, 'value':0x5555},
            'bf_tx_mbist_1_pat':     {'group':'bf_tx', 'addr':0x0146, 'size':2, 'value':0xaaaa},
            'bf_tx_mbist_2p_sel':    {'group':'bf_tx', 'addr':0x0149, 'size':1, 'value':0x00},
            'bf_tx_mbist_en':        {'group':'bf_tx', 'addr':0x014a, 'size':2, 'value':0x0000},
            'bf_tx_mbist_result':    {'group':'bf_tx', 'addr':0x014c, 'size':2, 'value':0x0000},
            'bf_tx_mbist_done':      {'group':'bf_tx', 'addr':0x014e, 'size':2, 'value':0x0000},
            #
            'bf_rx_mbist_0_pat':     {'group':'bf_rx', 'addr':0x01A4, 'size':2, 'value':0x5555},
            'bf_rx_mbist_1_pat':     {'group':'bf_rx', 'addr':0x01A6, 'size':2, 'value':0xaaaa},
            'bf_rx_mbist_2p_sel':    {'group':'bf_rx', 'addr':0x01A9, 'size':1, 'value':0x00},
            'bf_rx_mbist_en':        {'group':'bf_rx', 'addr':0x01Aa, 'size':2, 'value':0x0000},
            'bf_rx_mbist_result':    {'group':'bf_rx', 'addr':0x01Ac, 'size':2, 'value':0x0000},
            'bf_rx_mbist_done':      {'group':'bf_rx', 'addr':0x01Ae, 'size':2, 'value':0x0000},

            'bf_tx_awv_ptr':         {'group':'bf_tx', 'addr':0x0142, 'size':1,  'value':0x00},
            'bf_rx_awv_ptr':         {'group':'bf_rx', 'addr':0x01A2, 'size':1,  'value':0x00},
            'bf_tx_awv':             {'group':'bf_tx', 'addr':0x0800, 'size':64*32, 'value':0x0000},
            'bf_rx_awv':             {'group':'bf_rx', 'addr':0x1000, 'size':64*32, 'value':0x0000},
        }
        
