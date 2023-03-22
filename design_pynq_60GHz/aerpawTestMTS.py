from pynq import Overlay
from aerpawFPGAController import *


class objTest():
    def __init__(self):
        self.bitStreamAERPAW = 'aerpawFPGA_v46_8_128_1536_D1.bit'
        self.lmk = "_8_128_v2"
        self.lmx = "_128_1536_v0"  
        
        self.bitStreamAERPAW = 'aerpawFPGA_v46_8_192_1536_D1.bit'
        self.lmk = "_8_192_v0"
        self.lmx = "_192_1536_v0" 
       
        
        self.folderAERPAW = '/home/xilinx/jupyter_notebooks/aerpaw/'
        print("Hello AERPAW User")
        print('=================================')
        print('=================================')
        print('AERPAW folder: ' + self.folderAERPAW)
        print('FGPA bitsteam: ' + self.bitStreamAERPAW)
        print('=================================')
        print('=================================')

        print("Loading the FGPA bitstream")
        overlay = Overlay(self.folderAERPAW+self.bitStreamAERPAW)
        print("done")
        
        print("Starting the FPGA controller")
        self.fgpaControllerObj = fgpaController(overlay,self.lmk,self.lmx)
        print("done")
        
    
    
    
objTestObj = objTest()