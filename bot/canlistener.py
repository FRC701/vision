#!/usr/bin/python3

import threading
import can
import sys
from can import Message
import pprint

class Canlistener(threading.Thread):
    parent=None
    def __init__(self,parent=None):
        threading.Thread.__init__(self)
        self.parent=parent

    def run(self):
        can_interface = 'can0'
        for message in can.interface.Bus(can_interface, bustype='socketcan_native'):
            #print("id",message.arbitration_id)
            if message.arbitration_id == 0x07011C00:
                print("found it", message)
                if(self.parent is not None):
                    self.parent.send_data()
                else:
                    print("sending fake data")
                    bus2=can.interface.Bus(can_interface, bustype='socketcan_native')
                    msg = can.Message(0x07011400, [10, 20, 0, 1, 3, 1, 4, 1], False)
                    print("message being sent:",msg)
                    bus2.send(msg)



if __name__ == '__main__':
    clistener = Canlistener()
    try:
       clistener.start()
       clistener.join()
    except KeyboardInterrupt:
       sys.exit(1)
