#!/bin/python
import os
import time
import dropbox


try:
    dbx = dropbox.client.DropboxClient('Czqnuz6_Uy4AAAAAAAPVNIw6sEDYZWBs3gS6AOE1SwgDJq9VgkvBH-majbNjpadI')
    print ('linked account: ', dbx.account_info())
except Exception as e:
    online=False
nm = str(time.time())
#os.system("avconv -f video4linux2 -s 1280x960 -i /dev/video0 " + nm + ".avi")


pth="test.avi"
print "file exists:",os.path.isfile(pth)
try:
    f= open(pth, 'rb')
    dbx.put_file('/vanden/test/test.avi',f)
except Exception as e:
    print "error sending file ",e
