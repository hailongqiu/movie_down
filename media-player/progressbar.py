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


from dtk.ui.theme import ui_theme
from dtk.ui.draw import draw_hlinear, draw_pixbuf
from dtk.ui.utils import color_hex_to_cairo
from skin import app_theme
import gtk
import gobject


class ProgressBar(gtk.Button):
    __gsignals__ = {
        "set-value-event":(gobject.SIGNAL_RUN_LAST,
                        gobject.TYPE_NONE,(gobject.TYPE_INT,)),
        }    
    def __init__(self, max=100, width=6, 
                 point_normal_pixbuf = app_theme.get_pixbuf("progressbar/point.png"),
                 # point_hvoer = app_theme.get_pixbuf("progressbar/point_hvoer.png"),
                 # point_press = app_theme.get_pixbuf("progressbar/point_press.png")
                 ):
        gtk.Button.__init__(self)
        # init value.
        self.__value = 0
        self.drag = False
        self.max = max
        #
        self.point_normal_pixbuf = point_normal_pixbuf.get_pixbuf()
        #
        self.set_size_request(-1, self.point_normal_pixbuf.get_height())
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        # self.connect("")
        self.connect("expose-event", self.progressbar_expose_event)
        self.connect("button-press-event", self.progressbar_press_event)
        self.connect("button-release-event", self.progressbar_release_event)
        self.connect("motion-notify-event", self.progressbar_motion_notify_event)
        
    def progressbar_expose_event(self, widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        self.draw_bg(cr, rect)
        self.draw_fg(cr, rect)
        self.draw_point(cr, rect)
        return True
    
    def draw_bg(self, cr, rect):    
        # bg.背景色
        r, g, b = color_hex_to_cairo('#808080')
        cr.set_source_rgba(r, g, b, 0.8)
        cr.rectangle(rect.x, rect.y, rect.width, rect.height)
        cr.fill()
        
    def draw_fg(self, cr, rect):    
        # fg. 前景 渐变颜色.
        color = ui_theme.get_shadow_color("menu_item_select").get_color_info()[0][1][0]
        shadow_color = [(0.0, (color, 1.0)),
                        (0.7, (color, 0.7)),
                        (1.0, (color, 0.2))]        
        draw_hlinear(cr, rect.x, rect.y, int(float(self.value) / self.max * rect.width), rect.height,
                     shadow_color          
                     )        
    
    def draw_point(self, cr, rect):    
        draw_pixbuf(cr, self.point_normal_pixbuf, 
                    rect.x + int(float(self.value) / self.max * rect.width) - self.point_normal_pixbuf.get_width()/2, rect.y)
        
    def progressbar_press_event(self, widget, event):
        self.value =  (float((event.x)) / float(widget.allocation.width) * self.max) # get value.
        self.drag = True
        # print "press value:", self.value
        self.emit("set-value-event", self.value)
        
    def progressbar_release_event(self, widget, event):    
        self.drag = False
        
    def progressbar_motion_notify_event(self, widget, event):    
        if self.drag:
            self.value = max(min(self.max, (float((event.x)) / float(widget.allocation.width) * self.max)), 0) # get value.
            # print "motion value:", self.value
            self.emit("set-value-event", self.value)
            
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
        self.queue_draw()     
        
    @value.getter        
    def value(self):
        return self.__value
        
    @value.deleter
    def value(self):
        del self.__value        

        
if __name__ == "__main__":        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.connect("destroy", lambda w : gtk.main_quit())
    win.set_size_request(500, 8)
    pb = ProgressBar(3350)    
    win.add(pb)
    win.show_all()
    gtk.main()
    
