#
# Control China Camera Mount
#
# requires: Python 3
# requires: pyserial

# documentation about the "PELCO" protocol may be found here:
#  - https://www.commfront.com/pages/pelco-d-protocol-tutorial
#  - https://www.codeproject.com/Articles/8034/Pelco-P-and-D-protocol-implementation-in-C

SPEED_SLOW = 1
SPEED_MEDIUM = 2
SPEED_HIGH = 3

class pelco_mount():

    def __init__(self,p):
        self._outport = p
        self._adr = 1
    
    #
    # Actions
    #
    def pan_right(self):
        self._outport.write(self.msg_pan_right())
        
    def pan_left(self):
        self._outport.write(self.msg_pan_left())

    def pan_down(self):
        self._outport.write(self.msg_pan_down())
        
    def pan_up(self):
        self._outport.write(self.msg_pan_up())
                
    def stop_moving(self):
        self._outport.write(self.msg_pan_stop())
        
    def test_init(self):
        self._outport.write(self.msg_test_init())
        
    #    
    # Messages    
    #
    def msg_test_init(self):
        return self.msg_go_pre(18)
    
    def msg_factory_default(self):
        return self.msg_set_pre(20)
        
    def msg_go_home(self):
        return self.msg_go_pre(14)
        
    def msg_set_speed(self,speed):
        if speed==SPEED_SLOW:
            return self.msg_set_pre(15)
        elif speed==SPEED_MEDIUM:
            return self.msg_set_pre(16)
        elif speed==SPEED_HIGH:
            return self.msg_set_pre(17)
        else: 
            throw(Exception("invalid speed setting"))
        
    def msg_set_pre(self,nr):
        cmdbytes = [0,0x03,0x00,nr]  # "set preset"
        return self._makemsg(cmdbytes)
        
    def msg_go_pre(self,nr):
        cmdbytes = [0,0x07,0x00,nr]  # "goto preset"
        return self._makemsg(cmdbytes)
        
    def msg_pan_right(self):
        cmdbytes = [0,0x02,0x10,0x01]  # pan right
        return self._makemsg(cmdbytes)
        
    def msg_pan_left(self):
        cmdbytes = [0,0x04,0x10,0x01]  # pan left
        return self._makemsg(cmdbytes)

    def msg_pan_up(self):
        cmdbytes = [0,0x08,0x10,0x01] 
        return self._makemsg(cmdbytes)

    def msg_pan_down(self):
        cmdbytes = [0,0x10,0x10,0x01] 
        return self._makemsg(cmdbytes)

    def msg_pan_stop(self):
        cmdbytes = [0,0x00,0x00,0x00]
        return self._makemsg(cmdbytes)

    #
    # internal helper functions
    #
    def _makemsg(self,cmd):
        """
        Aus den Command-Bytes eine PELCO-D Nachricht zusammenstellen.
        """
        binmsg = bytes( [0xff, self._adr] + cmd )
        binmsg = binmsg + bytes([self.calc_checksum_pelco_d(binmsg)])
        return binmsg
        
    def calc_checksum_pelco_d(self,m):
        """
        Summe modulo 256 der übergebenen Bytes ab Pos. 2 ausrechnen.
        """
        r = 0
        for i in m[1:]:
            r = r + i
        return r % 256
