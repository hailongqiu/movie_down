#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 爱搜影, Inc.
#               2012 暴风
#
# Author:     暴风         <qw85525006@sina.com>
# Maintainer: 暴风,五彩书生  
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

import os
import gtk
from widget.navigation import Navigation
from widget.searchbar import SearchBar
from widget.searchinfo import SearchInfo
from widget.function import draw_pixbuf
from qvod_scan import QvodScan

FORM_WIDTH, FORM_HEIGHT = 800, 500

class QvodScanWidget(gtk.ScrolledWindow): 
    def __init__(self, pixbuf_file="widget/theme/background/wall.jpg"):
        gtk.ScrolledWindow.__init__(self)
        # init value.
        self.qvod = QvodScan()   
        if pixbuf_file:
            self.bg_pixbuf = gtk.gdk.pixbuf_new_from_file(pixbuf_file)
        # 
        self.init_navigation()
        self.init_search_bar()
        self.init_search_info()
        #
        self.main_vbox = gtk.VBox()
        self.add_with_viewport(self.main_vbox)
        #                
        self.main_vbox.pack_start(self.nav_igation, False, False)
        self.main_vbox.pack_start(self.search_bar_ali, False, False)
        self.main_vbox.pack_start(self.search_info_ali, False, False)
        self.main_vbox.connect("expose-event", self.searchbar_expose_event)
        
    def searchbar_expose_event(self, widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        try:
            pixbuf = self.bg_pixbuf.scale_simple(rect.width, rect.height, gtk.gdk.INTERP_BILINEAR)
            draw_pixbuf(cr, pixbuf, rect.x, rect.y)
        except Exception, e:    
            # print "图片加载错误!!", e
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.fill()

    def init_navigation(self):    
        self.nav_igation = Navigation(["首页", "动作片", "纪录片", "喜剧片",
                                       "科幻片", "爱情片", "战争片", "恐怖片",
                                       "综艺其它", "剧情片", "大陆剧", "港台剧",
                                       "欧美剧", "日韩剧", "音乐", "QMV高清"])
        self.nav_igation.connect("select-index-event", self.navigation_selece_index_event)
        
    def init_search_bar(self):            
        self.search_bar_ali = gtk.Alignment()
        #
        try:
            self.bg_pixbuf
            has_frame = False
        except:    
            has_frame = True
        #
        self.search_bar = SearchBar(has_frame)
        self.search_bar_ali.add(self.search_bar)        
        self.search_bar_ali.set(0.9, 0, 0.418, 0)
        self.search_bar_ali.set_padding(10, 10, 0, 0)
        
    def init_search_info(self): 
        self.search_info_ali = gtk.Alignment()
        self.search_info = SearchInfo()
        self.search_info.save_info_btn.connect("select-index-event", self.save_info_btn_select_index_event)
        self.search_info_ali.add(self.search_info)
        self.search_info_ali.set(0.9, 0, 0.4, 0)
        self.search_info_ali.set_padding(50, 0, 0, 0)
        
    def save_info_btn_select_index_event(self, width, index, title):    
        print "index:", index
        print "text:", title
        
    def navigation_selece_index_event(self, widget, index, title):
        print "index:", index
        print "text:", title
        
    
