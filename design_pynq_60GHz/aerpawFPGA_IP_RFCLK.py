#   Copyright (c) 2021, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import glob
import re
import struct
from pathlib import Path
from collections import defaultdict

__author__ = "Yun Rock Qu, Lewis Brown"
__copyright__ = "Copyright 2021, Xilinx"
__email__ = "pynq_support@xilinx.com"


board = os.environ['BOARD']

_Config = defaultdict(dict)

lmk_devices = []
lmx_devices = []

def _write_LMK_regs(reg_vals, lmk):

    """Write values to the LMK registers.

    This is an internal function.

    Parameters
    ----------
    reg_vals: list
        A list of 32-bit register values (LMK clock dependant number of values).
        LMK04208 (ZCU111) = 32 registers, num_bytes = 4
        LMK04832 (RFSoC2x2) = 125 registers, num_bytes = 3
    lmk: dictionary
        An instance of lmk_devices
        
    This function opens spi_device at /dev/spidevB.C and writes the register values stored in reg_vals.
    Number of bytes written is board dependant. 

    """   
    with open(lmk['spi_device'], 'rb+', buffering=0) as f:
        for v in reg_vals:
            data = struct.pack('>I', v)
            if lmk['num_bytes'] == 3:
                f.write(data[1:])
            else:
                f.write(data)
    
def _write_LMX_regs(reg_vals, lmx):
    """Write values to the LMX registers.

    This is an internal function.

    Parameters
    ----------
    reg_vals: list
        A list of 113 32-bit register values.
        
    reg_vals: list
        A list of 32-bit register values.
       LMX2594 (ZCU111 and RFSoC2x2) = 113 registers
    lmx: dictionary
        An instance of lmx_devices
        
    This function opens spi_device at /dev/spidevB.C and writes the register values stored in reg_vals.
    LMX must be reset before writing new values.
    """
    
    with open(lmx['spi_device'], 'rb+', buffering=0) as f:
        # Program RESET = 1 to reset registers.
        reset = struct.pack('>I', 0x020000)
        f.write(reset[1:])
        
        # Program RESET = 0 to remove reset.
        remove_reset = struct.pack('>I', 0)
        f.write(remove_reset[1:])
        
        # Program registers as shown in the register map in REVERSE order from highest to lowest
        for v in reg_vals:
            data = struct.pack('>I', v)
            f.write(data[1:])
            
        # Program register R0 one additional time with FCAL_EN = 1 
        # to ensure that the VCO calibration runs from a stable state.
        stable = struct.pack('>I', reg_vals[112])
        f.write(stable[1:])
        
        
def _set_LMX_clks(lmxParameters, lmx):
    """Set LMX chip frequency.
    
    This is an internal function.

    Parameters
    ----------
    LMX_freq: float
        The frequency for the LMX PLL chip.
    lmx: dictionary
        Contains the instance of lmx_devices.
        
    This function performs a check to ensure that lmx_freq is valid 
    and passes the corresponding register list to _write_LMX_regs
    """
    
    lmxExtension = '_' + str(lmxParameters['fpl']) + '_' + str(lmxParameters['frfdc']) + '_' + lmxParameters['tag']
    if lmxExtension not in _Config[lmx['compatible']]:
        raise RuntimeError('Not valid LMX file:' + lmxExtension)
    else:
        print('LMX extension: ' + lmxExtension[1:])
        _write_LMX_regs(_Config[lmx['compatible']][lmxExtension], lmx)
        
def _set_LMK_clks(lmkParameters, lmk):
    """Set LMK chip frequency.
    
    This is an internal function.

    Parameters
    ----------
    LMK_freq: float
        The frequency for the LMK chip.
    lmk: dictionary
        Contains the instance of lmk_devices.
        
    This function performs a check to ensure that lmk_freq is valid
    and passes the corresponding register list to _write_LMK_regs 
    """
    #print(lmk_freq)
    #print(_Config)
    lmkExtension = '_' + str(lmkParameters['fsysref']) + '_' + str(lmkParameters['fpl']) + '_' + lmkParameters['tag']
    
    if lmkExtension not in _Config[lmk['compatible']]:
        raise RuntimeError('Not valid LML file:' + lmkExtension)
    else:
        print('LMK extension: ' + lmkExtension[1:])
        _write_LMK_regs(_Config[lmk['compatible']][lmkExtension], lmk)
        
def _get_spidev_path(dev):
    spidev = list(dev.glob('spidev/*'))[0]
    return Path('/dev') / spidev.name

def _spidev_bind(dev):
    (dev / 'driver_override').write_text('spidev')
    Path('/sys/bus/spi/drivers/spidev/bind').write_text(dev.name)
    
        
def _find_devices():
    """
    Internal function to find lmk and lmx devices from the device tree and populate /dev/spidevB.C
    
    Also fills global variables lmk_devices and lmx_devices.
    """
    global lmk_devices, lmx_devices
    
    # loop for each SPI device on the device tree
    for dev in Path('/sys/bus/spi/devices').glob('*'):
        # read the compatible string from the device tree, containing name of chip, e.g. 'ti,lmx2594'
        # strip the company name to store e.g. 'lmx2594'
        compatible = (dev / 'of_node' / 'compatible').read_text()[3:-1]
        
        # if not lmk/lmx, either non-clock SPI device or compatible is empty
        if compatible[:3] != 'lmk' and compatible[:3] != 'lmx':
            continue
        else:
            # call spidev_bind to bind /dev/spidevB.C
            if (dev / 'driver').exists():
                (dev / 'driver' / 'unbind').write_text(dev.name)
            _spidev_bind(dev)
            
            # sort devices into lmk_devices or lmx_devices
            if compatible[:3] == 'lmk':
                lmk_dict = {'spi_device' : _get_spidev_path(dev), 
                            'compatible' : compatible, 
                            'num_bytes' : struct.unpack('>I', (dev / 'of_node' / 'num_bytes').read_bytes())[0]}
                lmk_devices.append(lmk_dict)
            else:
                lmx_dict = {'spi_device' : _get_spidev_path(dev), 
                            'compatible' : compatible}
                lmx_devices.append(lmx_dict)
                
    if lmk_devices == []:
        raise RuntimeError("SPI path not set. LMK not found on device tree. Issue with BSP.")
    if lmx_devices == []:
        raise RuntimeError("SPI path not set. LMX not found on device tree. Issue with BSP.")
        

def set_ref_clks(lmkParameters, lmxParameters):
    """Set all RF data converter tile reference clocks to a given frequency.

    LMX chips are downstream so make sure LMK chips are enabled first.

    Parameters
    ----------
    lmk_freq: float
        The frequency for the LMK clock generation chip.
    lmx_freq: float
        The frequency for the LMX PLL chip.
        
    lmk_devices: list of dictionaries
        For each lmk device on the board, stores {spi_device, compatible, num_bytes}
        ZCU111: 1 device
        RFSoC2x2: 1 device
    lmx_devices: list of dictionaries
        For each lmx device on the board, stores {spi_device, compatible}
        ZCU111: 3 devices
        RFSoC2x2: 2 devices (ADC and DAC)
        
    spi_device: location of /dev/spidevB.C
    compatible: name of lmk/lmx device
        ZCU111: lmk04208, lmx2594
        RFSoC2x2: lmk04832, lmx2594
    num_bytes: number of lmk bytes to write
        ZCU111: 4 bytes
        RFSoC2x2: 3 bytes

    """
    # lmk_devices and lmx_devices are global variables, only need to fill once
    # then store all register values from txt files, again only once
    if lmk_devices == [] and lmx_devices == []:    
        _find_devices()
        _read_tics_output()

    for lmk in lmk_devices:
        _set_LMK_clks(lmkParameters, lmk)
    for lmx in lmx_devices:
        _set_LMX_clks(lmxParameters, lmx)


def _read_tics_output():
    """Read all the TICS register values from all the txt files.
    
    Fill a single dictionary with dictionaries for each chip.
    Can store multiple frequencies per chip.

    Reading all the configurations from the current directory. We assume the
    file has a format `CHIPNAME_frequency.txt`.

    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    all_txt = glob.glob(os.path.join(dir_path, '*.txt'))
    
    print('Available txt files in directory will be scanned (LMK04832_fsysref_fpl_vXX.txt and LMX_fpl_frfdc_vXX.txt files must be in the directory.):')
    for s in all_txt:
        txtName = s.lower().split('/')[-1].strip('.txt')
        if txtName[0:2] == 'lm' or txtName[0:2] == 'lk':
            try:
                chip, freqIn, freqOut, tag = s.lower().split('/')[-1].strip('.txt').split('_')
                print([chip, freqIn, freqOut, tag])

                with open(s, 'r') as f:
                    lines = [l.rstrip("\n") for l in f]

                    registers = []
                    for i in lines:
                        m = re.search('[\t]*(0x[0-9A-F]*)', i)
                        registers.append(int(m.group(1), 16),)

                _Config[chip]['_'+str(freqIn)+'_'+str(freqOut)+'_'+tag] = registers                
            except:
                print(txtName + ' is not a properly named LMX or LMK file.')


                

