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

from function import draw_text, draw_pixbuf, alpha_color_hex_to_cairo
import gtk

'''MVC模式'''

class ListView(gtk.ScrolledWindow):
    def __init__(self, 
                 titles_pixbuf="widget/theme/listview/title.png",
                 bg_pixbuf="widget/theme/listview/bg.png"):
        gtk.ScrolledWindow.__init__(self)        
        frame_pixbuf="theme/progressbar/frame.png"
        fg_pixbuf="theme/progressbar/fg.png"
        # init values.
        self.text_color = ("#FFFFFF", 1)
        self.font_size = 10
        # init select values.
        self.select_index = 0
        self.select_color = ("#FFFFFF", 0.2)
        self.selectt_height = 30
        # init clicked values.
        self.clicked_index = None
        self.clicked_color = ('#CCCCFF', 0.7)        
        # init titles values.
        self.titles_pixbuf = gtk.gdk.pixbuf_new_from_file(titles_pixbuf)
        self.titles_pb_x_pdding = 285
        # init progressbar values.
        self.pb_w = 350
        self.pb_h = 20
        self.fg_w = self.pb_w - 8
        self.fg_h = self.pb_h - 7
        self.value = 50        
        self.frame_pixbuf = gtk.gdk.pixbuf_new_from_file(frame_pixbuf)
        self.fg_pixbuf = gtk.gdk.pixbuf_new_from_file(fg_pixbuf)
        #
        self.bg_pixbuf = gtk.gdk.pixbuf_new_from_file(bg_pixbuf)
        self.draw_main_gui = gtk.Button()
        self.draw_main_gui.set_size_request(1200, 1200)
        self.draw_main_gui.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.draw_main_gui.connect("expose-event", self.list_view_expose_event)
        self.draw_main_gui.connect("button-press-event", self.list_view_button_press_event)
        self.draw_main_gui.connect("motion-notify-event", self.list_view_motion_notify_event)
        self.add_with_viewport(self.draw_main_gui)        
        
    def list_view_motion_notify_event(self, widget, event):    
        self.check_select_darw(event.y)
        
    def list_view_button_press_event(self, widget, event):    
        self.check_clicked_draw(event.y)
        
    def check_clicked_draw(self, y):    
        index = int(y / self.selectt_height)
        if index:
            self.clicked_index = index
        self.queue_draw()
        
    def check_select_darw(self, y):    
        index = int(y / self.selectt_height)
        if index == 0:
            index = 1
        self.select_index = index
        self.queue_draw()
    
    def list_view_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        # draw background.
        self.draw_background(cr, rect)
        # draw select rectangle.
        self.draw_select_rectangle(cr, rect)
        # darw clicked rectangle.
        self.draw_clicked_rectangle(cr, rect)
        # draw titles.
        self.draw_titles(cr, rect)
        # test widgets.
        self.draw_progressbar(cr, rect, value=70, x=self.titles_pb_x_pdding, y=self.selectt_height + 5)
        self.draw_progressbar(cr, rect, value=80, x=self.titles_pb_x_pdding, y=2 * self.selectt_height + 5)
        self.draw_progressbar(cr, rect, value=60, x=self.titles_pb_x_pdding, y=3 * self.selectt_height + 5)
        self.draw_progressbar(cr, rect, value=60, x=self.titles_pb_x_pdding, y=4 * self.selectt_height + 5)
        self.draw_progressbar(cr, rect, value=60, x=self.titles_pb_x_pdding, y=5 * self.selectt_height + 5)
        return True
                
    def draw_background(self, cr, rect):
        bg_pixbuf = self.bg_pixbuf.scale_simple(rect.width, rect.height, gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, bg_pixbuf, rect.x, rect.y)
            
    def draw_select_rectangle(self, cr, rect):    
        if self.select_index: # 0 不画出来.
            self.draw_rectangle(cr, rect, self.select_index, self.select_color)
        
    def draw_clicked_rectangle(self, cr, rect):    
        if self.clicked_index != None: # None 不画出来.
            self.draw_rectangle(cr, rect, self.clicked_index, self.clicked_color)
        
    def draw_rectangle(self, cr, rect, index, color):    
        cr.set_source_rgba(*alpha_color_hex_to_cairo(color))
        cr.rectangle(rect.x,
                     rect.y + index * self.selectt_height, 
                     rect.width,
                     self.selectt_height)
        cr.fill()
        
    def draw_titles(self, cr, rect):                    
        # draw file name.
        name_pixbuf = self.titles_pixbuf.scale_simple(180, self.selectt_height, gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, name_pixbuf, rect.x - 10, rect.y)
        draw_text(cr, rect.x + 80, rect.y + 13, "文件名", ("#FFFFFF", 1.0), 10)
        # draw size.
        size_pixbuf = self.titles_pixbuf.scale_simple(120, self.selectt_height, gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, size_pixbuf, rect.x + name_pixbuf.get_width() - 18, rect.y)
        draw_text(cr, rect.x + name_pixbuf.get_width() + 45, rect.y + 13, "文件大小", ("#FFFFFF", 1.0), 10)
        # draw down progressbar.
        pb_pixbuf = self.titles_pixbuf.scale_simple(380, self.selectt_height, gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, pb_pixbuf, rect.x + name_pixbuf.get_width() + size_pixbuf.get_width() - 30, rect.y)
        draw_text(cr, rect.x + name_pixbuf.get_width() + size_pixbuf.get_width() + 45, rect.y + 13, "下载进度", ("#FFFFFF", 1.0), 10)        
        # draw down state.
        state_pixbuf = self.titles_pixbuf.scale_simple(rect.width, self.selectt_height, gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, state_pixbuf, rect.x + 500, rect.y)        
        
    def draw_progressbar(self, cr, rect, value, x=0, y=0):
        frame_pixbuf = self.frame_pixbuf.scale_simple(self.pb_w, self.pb_h, 
                                                      gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, frame_pixbuf, rect.x + x, rect.y + y)
        #
        if self.value > 0:
            fg_pixbuf = self.fg_pixbuf.scale_simple(int(value * self.fg_w / 100), 
                                                    self.fg_h,
                                                    gtk.gdk.INTERP_BILINEAR)
            draw_pixbuf(cr, fg_pixbuf, 
                        rect.x + 4 + x, rect.y + 3 + y)
        # text show.    
        color = ("#FFFFFF", 0.5)
        font_size =  9
        draw_text(cr, 
                  rect.x + self.pb_w/2 + x, 
                  rect.y + self.pb_h/2 - 1 + y, 
                  str(value) + "%", color, font_size)

if __name__ == "__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(500, 500)
    win.connect("destroy", lambda w : gtk.main_quit())
    win.add(ListView("theme/listview/title.png", "theme/listview/bg.png"))
    win.show_all()
    gtk.main()
    
