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
            if message.arbitration_id == 33821708:
                print("found it", message)
                if(self.parent is not None):
                    self.parent.send_data()



if __name__ == '__main__':
    clistener = Canlistener()
    try:
       clistener.start()
       clistener.join()
    except KeyboardInterrupt:
       sys.exit(1)
