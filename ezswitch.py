#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: 2010 Oct 11 05:58:29 PM CST
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

__version__ = "1.2"
__revision__ = '0.8.2'
__author__ = "Yi-Feng Tzeng"
__authorcontact__ = "yftzeng@gmail.com"
__website__ = "http://antbsd.twbbs.org"

import os, sys, re
import commands
import subprocess

default_mode = "auto"
#default_mode = "1280x800"

def main():
    global default_mode

    xrandr_output = map(lambda x: x.split(' ')[0] + ':' + x.split(' ')[1], commands.getoutput('xrandr').split('\n'))
    output = []
    for i in xrandr_output:
        if i == 'default:connected':
            os.system("zenity --warning --title='提示' --text 'This script only support laptop'")
            sys.exit()
        if i != ':' and i != 'Screen:0:' and i != 'LVDS:connected' and i != 'LVDS1:connected':
            if i.split(':')[1] == 'connected':
                output.append(i.split(':')[0])

    default_name = "LVDS"
    mon_output = map(lambda x: x.split(' ')[0] + ':' + x.split(' ')[3], commands.getoutput('xrandr').split('\n'))
    mon = []
    for i in mon_output:
        if re.search(r'x', i):
            mon.append(i.split(':')[1])
        if re.search(r'LVDS1', i):
            default_name = "LVDS1"

    if (len(output) == 0 or len(mon) == 0):
        os.system("zenity --warning --title='提示' --text 'No external screen found, please check if it is not connected'")
    else:
        str = "zenity --width=400 --height=240 --list --radiolist --title='switch screen' --column='items' --column='summary' --column='details' "
        s = 0
        cmd = {}
        for i in range(len(mon)):
            if (s == 0):
                str+="TRUE "
            else:
                str+="FALSE "
            str+="'投影(" + mon[i] + ")' 'screen(" + mon[i] + ")' "
            cmd['投影(' + mon[i] + ')'] = "xrandr --output " + default_name + " --mode " + default_mode + " --pos 0x0 --output " + output[0] + " --mode " + mon[i] + " --right-of " + default_name
            s+=1
        str+="FALSE 'laptop' 'disconnect external screen'"
        cmd['本機'] = "xrandr --output " + output[0] + " --off"

        fout = subprocess.Popen(str, shell=True, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        selected = fout.stdout.readline().strip()

        for k, v in cmd.iteritems():
            if selected == k:
                os.system(v)

if __name__ == '__main__':
    main()

