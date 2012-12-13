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

import gtk
from function import draw_pixbuf

class ProgressBar(gtk.Button):
    def __init__(self, 
                 value = 100,
                 frame_pixbuf="theme/progressbar/frame.png",
                 fg_pixbuf="theme/progressbar/fg.png"):
        gtk.Button.__init__(self)
        # init value.
        self.pb_w = 350
        self.pb_h = 20
        self.fg_w = self.pb_w - 8
        self.fg_h = self.pb_h - 7
        self.value = value
        if value > 100:
            self.value = 100
        elif value < 0:
            self.value = 0            
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("expose-event", self.progressbar_expose_event)
        self.frame_pixbuf = gtk.gdk.pixbuf_new_from_file(frame_pixbuf)
        self.fg_pixbuf = gtk.gdk.pixbuf_new_from_file(fg_pixbuf)
        self.set_size_request(self.pb_w, self.pb_h)
        
        
    def set_value(self, value):    
        if 0 <= value <= 100:
            self.value = value
            self.queue_darw()
            
    def progressbar_expose_event(self, widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        #
        frame_pixbuf = self.frame_pixbuf.scale_simple(self.pb_w, self.pb_h, 
                                                      gtk.gdk.INTERP_BILINEAR)
        #
        draw_pixbuf(cr, frame_pixbuf, rect.x, rect.y)
        if self.value > 0:
            fg_pixbuf = self.fg_pixbuf.scale_simple(self.value * self.fg_w / 100, 
                                                self.fg_h,
                                                gtk.gdk.INTERP_BILINEAR)
            draw_pixbuf(cr, fg_pixbuf, rect.x + 4, rect.y + 3)
        return True
    
if __name__ == "__main__":    
    def win_expose_event(widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        pixbuf = gtk.gdk.pixbuf_new_from_file("theme/progressbar/bg.png").scale_simple(rect.width, rect.height, gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, pixbuf, rect.x, rect.y)
        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    fixed = gtk.Fixed()
    win.connect("destroy", lambda w : gtk.main_quit())
    fixed.add_events(gtk.gdk.ALL_EVENTS_MASK)
    fixed.connect("expose-event", win_expose_event)
    fixed.put(ProgressBar(120), 20, 50)
    fixed.put(ProgressBar(80), 20, 90)
    fixed.put(ProgressBar(40), 20, 130)
    win.add(fixed)
    win.show_all()
    gtk.main()
        
