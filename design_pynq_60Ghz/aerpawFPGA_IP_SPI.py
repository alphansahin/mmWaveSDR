from pynq import DefaultIP


class spiController(DefaultIP):
   
    def __init__(self, description):
        super().__init__(description=description)
        
    bindto = ['xilinx.com:ip:axi_quad_spi:3.2']

    
    @property
    def test1(self):
        return self.read(0x08)    

   
    @property
    def test2(self):
        return self.read(0x100)
    
    @test2.setter
    def test2(self, packetsize):
        self.write(0x100, packetsize)