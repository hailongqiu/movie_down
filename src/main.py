#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
from qvod_scan_gui import QvodScanWidget

if __name__ == "__main__":            
    def temp_nav_selece_index(widget, index):
        print index
        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("qvod搜索下载器")
    win.connect("destroy", lambda w : gtk.main_quit())
    win.set_size_request(980, 500)
    qvod_scan_widget = QvodScanWidget()
    
    win.add(qvod_scan_widget)
    win.show_all()
    gtk.main()
    
