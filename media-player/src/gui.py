#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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

from skin import app_theme
from dtk.ui.application import Application
from locales import _
import gtk

class GUI(object):
    '''Media Player GUI kernel code.核心界面代码'''
    def __init__(self):        
        '''application.'''
        self.app = Application(False)
        # application set.
        self.app.set_default_size(800, 500)
        # self.app.window.resize
        self.app.set_icon(app_theme.get_pixbuf("icon.ico"))
        self.app.set_skin_preview(app_theme.get_pixbuf("frame.png"))
        # set titlebar.
        self.app.add_titlebar(["theme", "menu", "max", "min", "close"],
                              app_theme.get_pixbuf("logo.png"),
                              _("Deepin Media Player"), " ", 
                              add_separator = False)
        #
        self.main_ali = gtk.Alignment()
        self.main_vbox = gtk.VBox()
        self.main_ali.add(self.main_vbox)
        self.main_ali.set(0, 0, 1.0, 1.0)
        self.main_ali.set_padding(0, 2, 2, 2)
        '''movie screen. 电影播放屏幕.'''
        # 播放屏幕和播放列表的HBOX.
        self.screen_and_play_list_hbox = gtk.HBox() 
        self.screen_frame = gtk.Alignment(0.0, 0.0, 1.0, 1.0)
        self.screen = gtk.DrawingArea()
        self.screen_frame.add(self.screen)
        #
        self.play_list = gtk.Button("播放列表")
        #
        self.screen_and_play_list_hbox.pack_start(self.screen_frame, True, True)
        self.screen_and_play_list_hbox.pack_start(self.play_list, False, False)
        #
        self.main_vbox.pack_start(self.screen_and_play_list_hbox, True, True)
        #
        self.app.main_box.pack_start(self.main_ali, True, True)
        
    def show_play_list(self):    
        self.screen_and_play_list_hbox.pack_start(self.play_list, False, False)
        
    def hide_play_list(self):    
        self.screen_and_play_list_hbox.remove(self.play_list)        
