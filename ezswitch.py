#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: 2009 Apr 28 04:53:50 PM CST
#
# LICENSE:
# ***************************************************************************
# * Copyright (c) 2009 Yi-Feng Tzeng                                        *
# *                                                                         *
# * Permission is hereby granted, free of charge, to any person obtaining   *
# * a copy of this software and associated documentation files (the         *
# * "Software"), to deal in the Software without restriction, including     *
# * without limitation the rights to use, copy, modify, merge, publish,     *
# * distribute, sublicense, and/or sell copies of the Software, and to      *
# * permit persons to whom the Software is furnished to do so, subject to   *
# * the following conditions:                                               *
# *                                                                         *
# * The above copyright notice and this permission notice shall be          *
# * included in all copies or substantial portions of the Software.         *
# *                                                                         *
# * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,         *
# * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF      *
# * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                   *
# * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE  *
# * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION  *
# * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION   *
# * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.         *
# ***************************************************************************


"""
"""

__version__ = "0.3"
__revision__ = '0.3.2'
__author__ = "Yi-Feng Tzeng"
__authorcontact__ = "yftzeng@gmail.com"
__website__ = "http://antbsd.twbbs.org"

import os, sys, re
import commands
import subprocess

def main():
    xrandr_output = map(lambda x: x.split(' ')[0] + ':' + x.split(' ')[1], commands.getoutput('xrandr').split('\n'))
    output = []
    for i in xrandr_output:
        if i == 'default:connected':
            os.system("zenity --warning --title='提示' --text '此程式僅支援筆記型螢幕, 並不支援桌上機型'")
            sys.exit()
        if i != ':' and i != 'Screen:0:' and i != 'LVDS:connected':
            if i.split(':')[1] == 'connected':
                output.append(i.split(':')[0])

    mon_output = map(lambda x: x.split(' ')[0] + ':' + x.split(' ')[3], commands.getoutput('xrandr').split('\n'))
    mon = []
    for i in mon_output:
        if re.search(r'x', i):
            mon.append(i.split(':')[1])
        if re.search(r'LVDS', i):
            break

    if (len(output) == 0 or len(mon) == 0):
        os.system("zenity --warning --title='提示' --text '沒有發現外接螢幕, 請檢查影像連接線是否正確接上您的電腦'")
    else:
        str = "zenity --width=400 --height=240 --list --radiolist --title='切換顯示器' --column='選擇' --column='簡述' --column='詳述' "
        s = 0
        cmd = {}
        for i in range(len(mon)):
            if (s == 0):
                str+="TRUE "
            else:
                str+="FALSE "
            str+="'投影(" + mon[i] + ")' '使用本機與外接螢幕(" + mon[i] + ")' "
            cmd['投影(' + mon[i] + ')'] = "xrandr --output LVDS --output " + output[0] + " --mode " + mon[i] + " --auto"
            s+=1
        str+="FALSE '本機' '只使用本機的螢幕'"
        cmd['本機'] = "xrandr --output " + output[0] + " --off"

        fout = subprocess.Popen(str, shell=True, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        selected = fout.stdout.readline().strip()

        for k, v in cmd.iteritems():
            if selected == k:
                os.system(v)

if __name__ == '__main__':
    main()

