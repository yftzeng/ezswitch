#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Last modified: 2011 Mar 07 04:49:44 PM CST
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

__version__ = "1.4.1"
__revision__ = '1.4.1'
__author__ = "Yi-Feng Tzeng"
__authorcontact__ = "yftzeng@gmail.com"
__website__ = "http://antbsd.twbbs.org/"

import os, sys, re
import commands
import subprocess

## Change language
#lang = "en"
lang = "zh-tw"
#lang = "zh-cn"

def i18n(str):
    global lang
    if str == 'title':
        if lang == "en":
            return 'Notice'
        elif lang == "zh-tw":
            return '提示'
        elif lang == "zh-cn":
            return '提示'
    if str == 'local':
        if lang == "en":
            return 'Local'
        elif lang == "zh-tw":
            return '本機'
        elif lang == "zh-cn":
            return '本机'
    if str == 'only-laptop':
        if lang == "en":
            return 'This program only support laptop'
        elif lang == "zh-tw":
            return '此程式僅支援筆記型螢幕, 並不支援桌上機型'
        elif lang == "zh-cn":
            return '此程式仅支援笔记本电脑, 并不支援桌上型电脑'
    if str == 'no-external-monitor':
        if lang == "en":
            return 'External monitor not found'
        elif lang == "zh-tw":
            return '沒有發現外接螢幕, 請檢查影像連接線是否正確接上您的電腦'
        elif lang == "zh-cn":
            return '没有发现外接视讯, 请检查影像连接线是否正确接上您的电脑'
    if str == 'change-monitor':
        if lang == "en":
            return 'ezswitch - Change monitor screen'
        elif lang == "zh-tw":
            return 'ezswitch - 切換顯示器'
        elif lang == "zh-cn":
            return 'ezswitch - 切换视讯'
    if str == 'choose':
        if lang == "en":
            return 'Choose'
        elif lang == "zh-tw":
            return '選擇'
        elif lang == "zh-cn":
            return '选择'
    if str == 'brief':
        if lang == "en":
            return "Brief"
        elif lang == "zh-tw":
            return "簡述"
        elif lang == "zh-cn":
            return "简述"
    if str == 'summary':
        if lang == "en":
            return "Summary"
        elif lang == "zh-tw":
            return "描述"
        elif lang == "zh-cn":
            return "描述"
    if str == 'projector':
        if lang == "en":
            return "Projector"
        elif lang == "zh-tw":
            return "投影"
        elif lang == "zh-cn":
            return "投影"
    if str == 'external':
        if lang == "en":
            return "External monitor"
        elif lang == "zh-tw":
            return "使用外接投影"
        elif lang == "zh-cn":
            return "使用外接视讯"
    if str == 'only-local':
        if lang == "en":
            return "Use local monitor"
        elif lang == "zh-tw":
            return "只使用本機的螢幕"
        elif lang == "zh-cn":
            return "仅使用笔记本视讯"

def getLVDSmode():
    xrandr_output = map(lambda x: x.split(' ')[0] + ':' + x.split(' ')[2], commands.getoutput('xrandr').split('\n'))
    for i in xrandr_output:
        if i[0:4] == "LVDS":
            return i.split(':')[1].split('+')[0]

def main():
    default_mode = getLVDSmode()

    xrandr_output = map(lambda x: x.split(' ')[0] + ':' + x.split(' ')[1], commands.getoutput('xrandr').split('\n'))
    output = []
    for i in xrandr_output:
        if i == 'default:connected':
            os.system("zenity --warning --title=" + i18n("title") + "--text '" + i18n("only-laptop") + "'")
            sys.exit()
        if i != ':' and i != 'Screen:0:' and i != 'LVDS:connected' and i != 'LVDS1:connected':
            if i.split(':')[1] == 'connected':
                output.append(i.split(':')[0])

    default_name = "LVDS"
    mon_output = map(lambda x: x.split(' ')[0] + ':' + x.split(' ')[3], commands.getoutput('xrandr').split('\n'))
    mon = []
    for i in mon_output:
        if re.search(r'x', i):
            item = i.split(':')[1]
            if item not in mon: mon.append(item)
        if re.search(r'LVDS1', i):
            default_name = "LVDS1"

    if (len(output) == 0 or len(mon) == 0):
        os.system("zenity --warning --title='" + i18n("title") + "' --text '" + i18n("no-external-monitor") + "'")
    else:
        str = "zenity --width=450 --height=380 --list --radiolist --title='" + i18n("change-monitor") + "' --column='" + i18n('choose') + "' --column='" + i18n("brief") + "' --column='" + i18n("summary") + "' "
        s = 0
        cmd = {}
        for i in range(len(mon)):
            if (s == 0):
                str+="TRUE "
            else:
                str+="FALSE "
            str+="'" + i18n('projector') + "(" + mon[i] + ")' '" + i18n('external') + "(" + mon[i] + ")' "
            cmd[i18n('projector') + "(" + mon[i] + ")"] = "xrandr --output " + default_name + " --mode " + default_mode + " --pos 0x0 --output " + output[0] + " --mode " + mon[i] + " --right-of " + default_name
            s+=1
        str+="FALSE '" + i18n("local") + "' '" + i18n('only-local') + "'"
        cmd['本機'] = "xrandr --output " + output[0] + " --off --output " + default_name + " --mode " + default_mode

        fout = subprocess.Popen(str, shell=True, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        selected = fout.stdout.readline().strip()

        for k, v in cmd.iteritems():
            if selected == k:
                os.system(v)
                break

if __name__ == '__main__':
    main()

