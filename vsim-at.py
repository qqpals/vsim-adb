#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
import re
import sys
import time
import os
from multiprocessing import Process

#vsim at command script configuration
at_set = 'at_set.sh'
at_cat = 'at_cat.sh'
at_check = 'at_check.sh'
at_result = 'at_result.txt'

vsim_at_command1 = ['adb shell ' + at_set,]
vsim_at_command_ret1 = ['',]
vsim_at_command2 = ['adb shell ' + at_check,]
vsim_at_command_ret2 = ['',]


def adb_command(command,command_ret=''):
    obj = subprocess.Popen(command, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out,err = obj.communicate()

    returncode = obj.returncode
    if returncode != 0:
        print('Command process error,errono is {}'.format(returncode))
        str_err = err.decode('utf-8')
        print(str_err)
        return 1

    if command_ret == '':
        return 0

    str=out.decode('utf-8')
    print(str)

    pattern = re.compile(command_ret,flags=re.M|re.S)
    n = pattern.match(str)


    if  n!= None:
        #print(n.group(0))
        return 0
    else:
        print('adb command:"{}" result not correct, please check mannually!'.format(command))
        return 1

def adb_check():
    ret = adb_command('adb devices', r'^List.*device$')
    if ret:
        exit()

def run_proc(command) :
    adb_command(command)
    exit()

if __name__ == '__main__':

    #Check adb connection
    adb_check()

    #Begin process adb shell command
    adb_command('adb root')
    if adb_command('adb push' + ' ' + at_set + ' ' + at_cat + ' ' + at_check + ' /bin'):
        exit()

    #Setting vsim
    for (com1, com_ret1) in  zip(vsim_at_command1,vsim_at_command_ret1) :
        adb_command(com1,com_ret1)

    #Waiting for module reboot
    time.sleep(15)
    adb_check()

    #checking the result
    """
    pid = os.fork()
    if pid == 0:
        adb_command('adb shell' + ' /bin/' + at_cat)
        exit()
    else:
        time.sleep(5)
        for (com2,com_ret2) in  zip(vsim_at_command2,vsim_at_command_ret2) :
            adb_command(com2, com_ret2)
            time.sleep(1)
    """
    p = Process(target = run_proc, args=('adb shell'+' /bin/'+at_cat,))
    p.start()

    time.sleep(5)
    for (com2,com_ret2) in  zip(vsim_at_command2,vsim_at_command_ret2) :
        adb_command(com2, com_ret2)
        time.sleep(1)

    p.terminate()
    p.join()

    #Get the at_result.txt
    adb_command('adb pull'+ ' /bin/' + at_result )
    try:
        with open(at_result, 'r', encoding = 'utf-8') as f:
            result = f.read()
            print(result)
    except:
        print("Open %s error!" % at_result)

    #Delete shell scripts
    adb_command('adb shell rm -rf' + ' /bin/' + at_set + ' /bin/' + at_cat +
            ' /bin/' + at_check + ' /bin/' + at_result )


