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
from function import draw_pixbuf
from sound.sound import sound_play

BACK_SPACE_KEY = 65288
TAB_KEY = 65289
CAPS_LOCK_KEY = 65509
SHIFT_LEFT_KEY = 65505
SHIFT_RIGHT_KEY = 65506
ENTER_KEY = 65293 
CTRL_LEFT_KEY = 65507
CTRL_RIGHT_KEY = 65508
ALT_LEFT_KEY = 65513
ALT_RIGHT_KEY = 65514

LEFT_KEY  = 65361
RIGHT_KEY = 65363
UP_KEY    = 65362
DOWN_KEY  = 65364

PAUP_KEY = 65365
PADN_KEY = 65366
HOME_KEY = 65360

F1, F2, F3, F4, F5, F6, F7,F8, F9, F10, F11, F12 = (65470, 65471, 65472, 65473, 65474, 65475, 65476, 65477, 65478, 65479, 65480, 65481)

class SearchBar(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        #
        self.bg_pixbuf = gtk.gdk.pixbuf_new_from_file("widget/theme/search/searchframe.png")
        #
        self.search_text = gtk.Entry()
        self.search_text.connect("key-press-event", self.search_text_key_sound)
        # self.search_text.set_has_frame(False)
        self.search_text.set_size_request(420, self.search_text.get_size_request()[1])
        self.search_btn_ali = gtk.Alignment()
        self.search_btn  = SearchBtn()
        self.search_btn_ali.add(self.search_btn)
        self.search_btn_ali.set_padding(4, 0, 0, 0)
        self.pack_start(self.search_text, False, False)
        self.pack_start(self.search_btn_ali, False, False)
    
    def search_text_key_sound(self, widget, event):    
        print event.keyval
        if event.keyval not in [BACK_SPACE_KEY, TAB_KEY, CAPS_LOCK_KEY, SHIFT_LEFT_KEY, SHIFT_RIGHT_KEY,
                                CTRL_LEFT_KEY, CTRL_RIGHT_KEY, ALT_LEFT_KEY, ALT_RIGHT_KEY, ENTER_KEY,
                                LEFT_KEY, RIGHT_KEY, UP_KEY, DOWN_KEY, HOME_KEY,
                                PAUP_KEY, PADN_KEY,
                                F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12]:
            sound_play.play("widget/theme/sound/type.wav")
            
class SearchBtn(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self)
        self.normal_pixbuf = gtk.gdk.pixbuf_new_from_file("widget/theme/search/search.png")
        self.hover_pixbuf  = self.normal_pixbuf.scale_simple(self.normal_pixbuf.get_width() + 5, self.normal_pixbuf.get_height() + 5, gtk.gdk.INTERP_BILINEAR)
        self.press_pixbuf  = self.normal_pixbuf
        #
        self.set_size_request(self.normal_pixbuf.get_width(), self.normal_pixbuf.get_height())
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("expose-event", self.searchbtn_expose_event)
        
    def searchbtn_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        #
        if widget.state == gtk.STATE_NORMAL:
            pixbuf = self.normal_pixbuf
        elif widget.state == gtk.STATE_PRELIGHT:
            pixbuf = self.hover_pixbuf
        elif widget.state == gtk.STATE_ACTIVE:
            pixbuf = self.press_pixbuf
        # draw state pixbuf.
        draw_pixbuf(cr, pixbuf, rect.x, rect.y)    
        return True
    
                
