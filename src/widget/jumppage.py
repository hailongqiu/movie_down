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
from function import new_draw_text
# 2807 条记录 1/94 页  第一页 上一页  1 2 3 4 5 6 7 8 下一页 最后一页

class JumpPage(gtk.HBox):
    def __init__(self, sum):
        gtk.HBox.__init__(self)
        # init values.
        self.sum = sum # 条记录
        self.sum_num = 8        
        self.end_page = self.sum_to_page_num(self.sum) # 最后的页码
        self.start_page = 1 # 开始的页码
        self.__current_page = self.start_page # 当前页码.
        self.info_text = "%s 条记录 %s/%s 页" # 信息显示text.
        self.info_color = "#000000"
        self.info_size = 10
        #
        self.start_page_btn = gtk.Button()
        self.end_page_btn = gtk.Button()
        self.info_text_btn = gtk.Button()
        self.jump_page_btn = gtk.Button()
        
        self.info_text_btn.connect("expose-event", self.info_text_btn_expose_event)
        self.start_page_btn.connect("expose-event", self.start_page_btn_expose_event)
        self.end_page_btn.connect("expose-event", self.end_page_btn_expose_event)
        self.jump_page_btn.connect("expose-event", self.jump_page_btn_expose_event)
        
        self.pack_start(self.info_text_btn, False, False)
        self.pack_start(self.start_page_btn, False, False)
        self.pack_start(self.jump_page_btn, False, False)
        self.pack_start(self.end_page_btn, False, False)
        
    def sum_to_page_num(self, sum):    
        end_page = sum / self.sum_num
        if (sum % self.sum_num) > 0:
            end_page += 1
        return end_page    
    
    def set_current_page(self, current_page):
        if self.start_page <= current_page <= self.end_page:
            self.__current_page = current_page
            return True
        return False
    
    def info_text_btn_expose_event(self, widget, event):     
        cr = widget.window.cairo_create()
        rect = widget.allocation
        w, h = new_draw_text(cr, 
                  rect.x, 
                  rect.y, 
                  self.info_text % (self.sum, self.__current_page, self.end_page), 
                  (self.info_color, 0.7), self.info_size)
        widget.set_size_request(w + 5, h)
        return True
        
    def start_page_btn_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        w, h = new_draw_text(cr, 
                         rect.x,
                         rect.y,
                         "第一页",
                         ("#000000", 0.7), self.info_size)
        widget.set_size_request(w + 5, h)
        return True
    
    def jump_page_btn_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        w, h = new_draw_text(cr, 
                         rect.x,
                         rect.y,
                         "1 2 3 4 5 7 8",
                         ("#000000", 0.7), self.info_size)
        widget.set_size_request(w + 5, h)
        return True
    
    def end_page_btn_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        w, h = new_draw_text(cr, 
                  rect.x,
                  rect.y,
                  "最后一页",
                  ("#000000", 0.7), self.info_size)
        widget.set_size_request(w + 10, h)
        return True
    
        
if __name__ == "__main__":    
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("测试页码跳转")
    win.set_size_request(500, 500)
    vbox = gtk.VBox()
    jump_page = JumpPage(1000)
    vbox.pack_start(gtk.Button("fdjskl"), False, False)
    vbox.pack_start(jump_page, False, False)
    vbox.pack_start(gtk.Button("fdjskl"), False, False)
    jump_page.set_current_page(10)
    win.connect("destroy", lambda w : gtk.main_quit())
    win.add(vbox)
    win.show_all()
    gtk.main()
