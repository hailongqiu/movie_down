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
import gobject
'''MVC模式'''

class ModeList(gobject.GObject):
    '''模式'''
    __gsignals__ = {        
        "update-data-event":(gobject.SIGNAL_RUN_LAST,
                             gobject.TYPE_NONE,(gobject.TYPE_INT, gobject.TYPE_INT, gobject.TYPE_STRING,))
        }    
    def __init__(self, items=[]):
        gobject.GObject.__init__(self)
        self.items = items
        
    def modify_data(self, row, column, data):    # row 行 column 列
        self.items[row][column] = data
        self.emit("update-data-event", row, column, data)
        
class ListView(gtk.ScrolledWindow):
    '''視圖'''
    def __init__(self, 
                 mode_list,
                 titles_pixbuf="widget/theme/listview/title.png",
                 bg_pixbuf="widget/theme/listview/bg.png"):
        gtk.ScrolledWindow.__init__(self)        
        frame_pixbuf="theme/progressbar/frame.png"
        fg_pixbuf="theme/progressbar/fg.png"
        # init mode list.
        self.mode_list = mode_list
        self.mode_list.connect("update-data-event", self.mode_list_update_data_event)
        self.index_sum = len(self.mode_list.items)
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
        self.pb_y_padding = 5
        self.frame_pixbuf = gtk.gdk.pixbuf_new_from_file(frame_pixbuf)
        self.fg_pixbuf = gtk.gdk.pixbuf_new_from_file(fg_pixbuf)
        # init file name values.
        self.file_y_pdding = 15
        self.file_name_x_padding = 80
        # init file size values.
        self.file_size_x_padding = self.file_name_x_padding + 150
        # init down state values.
        self.down_state_x_pdding = 700
        self.error_pixbuf = gtk.gdk.pixbuf_new_from_file("theme/listview/error.png")
        self.wait_pixbuf = gtk.gdk.pixbuf_new_from_file("theme/listview/wait.png")
        self.working_pixbuf = gtk.gdk.pixbuf_new_from_file("theme/listview/working.png")
        self.success_pixbuf = gtk.gdk.pixbuf_new_from_file("theme/listview/success.png")
        #
        self.bg_pixbuf = gtk.gdk.pixbuf_new_from_file(bg_pixbuf)
        self.draw_main_gui = gtk.Button()
        self.draw_main_gui.set_size_request(790, 1200)
        self.draw_main_gui.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.draw_main_gui.connect("expose-event", self.list_view_expose_event)
        self.draw_main_gui.connect("button-press-event", self.list_view_button_press_event)
        self.draw_main_gui.connect("motion-notify-event", self.list_view_motion_notify_event)
        self.add_with_viewport(self.draw_main_gui)                
        
    def mode_list_update_data_event(self, widget, row, column, data):
        # 數據修改,更改界面.
        self.draw_main_gui.queue_draw()
        
    def list_view_motion_notify_event(self, widget, event):    
        self.check_select_darw(event.y)
        
    def list_view_button_press_event(self, widget, event):    
        self.check_clicked_draw(event.y)
        
    def check_clicked_draw(self, y):    
        index = int(y / self.selectt_height)
        if index and index <= self.index_sum:
            self.clicked_index = index
            self.queue_draw()
            # self.emit()
        
    def check_select_darw(self, y):    
        index = int(y / self.selectt_height)
        if index == 0:
            index = 1
        if index <= self.index_sum:     
            self.select_index = index
            self.queue_draw()
            # self.emit()
    
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
        mode_index = 1
        for i in self.mode_list.items:                        
            self.list_vewi_cellrenderer(cr, rect, i, mode_index)            
            mode_index += 1
        return True

    def list_vewi_cellrenderer(self, cr, rect, i, mode_index):
        '''渲染端'''
        self.draw_file_name(cr, rect, name=i[0], 
                            x=self.file_name_x_padding, 
                            y=mode_index *self.selectt_height + self.file_y_pdding)
        self.draw_file_size(cr, rect, size=i[1], 
                            x=self.file_size_x_padding, 
                            y=mode_index *self.selectt_height + self.file_y_pdding)
        self.draw_progressbar(cr, rect, value=i[2], 
                              x=self.titles_pb_x_pdding, 
                              y=mode_index *self.selectt_height + self.pb_y_padding)
        self.draw_down_state(cr, rect, state=i[3], 
                             x=self.down_state_x_pdding, 
                             y=mode_index * self.selectt_height + self.file_y_pdding - self.error_pixbuf.get_height()/2)
        
    def draw_file_name(self, cr, rect, name, x=0, y=0):    
        name = name.decode("utf-8")
        if len(name) > 10:
            name = name[:4] + "..." + name[-5:]
        draw_text(cr, rect.x + x, rect.y + y, str(name), ("#000000", 1), 10)
        
    def draw_file_size(self, cr, rect, size, x=0, y=0):    
        draw_text(cr, rect.x + x, rect.y + y, str(size), ("#000000", 1), 10)
                
    def draw_down_state(self, cr, rect, state, x=0, y=0):    
        state_pixbuf = None
        if state == "error": # 错误
            state_pixbuf = self.error_pixbuf
        elif state == "success": # 下载完成
            state_pixbuf = self.success_pixbuf
        elif state == "wait":   # 等待
            state_pixbuf = self.wait_pixbuf
        elif state == "working": # 正在下载
            state_pixbuf = self.working_pixbuf
        #    
        if state_pixbuf:    
            draw_pixbuf(cr, state_pixbuf, rect.x + x, rect.y + y)
        else:    
            draw_text(cr, rect.x + x, rect.y + y, str(state), ("#000000", 1), 10)
        
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
        '''画litview标题'''
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
        draw_text(cr, rect.x + name_pixbuf.get_width() + size_pixbuf.get_width() + 155, rect.y + 13, "下载进度", ("#FFFFFF", 1.0), 10)        
        # draw down state.
        state_pixbuf = self.titles_pixbuf.scale_simple(rect.width, self.selectt_height, gtk.gdk.INTERP_BILINEAR)
        draw_pixbuf(cr, state_pixbuf, rect.x + 618, rect.y)        
        draw_text(cr, rect.x + name_pixbuf.get_width() + size_pixbuf.get_width() + 400, rect.y + 13, "状态", ("#FFFFFF", 1.0), 10) 
        
        
    def draw_progressbar(self, cr, rect, value, x=0, y=0):
        '''画进度条'''
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
    def test_modify_gui():
        mode_list.modify_data(0, 0, "沒人")
        mode_list.modify_data(0, 1, "100MB")
        mode_list.modify_data(0, 2, 88.9)
    # test mode list.
    mode_list = ModeList([["我来看看国产家大夫吧好", "500MB", 50, "wait"],
                          ["我的司機發送到佛教看來佛教所端口樓房倾国", "1GB", 70, "error"],
                          ["心三国", "128MB", 50, "wait"],
                          ["心三国", "128MB", 80.5, "working"],
                          ["心三国", "128MB", 100, "success"],
                          ["心三国", "128MB", 90.8, "wait"],
                          ["心三国", "128MB", 70.9, "working"],
                          ["心三国", "128MB", 60.9, "wait"],
                          ["心三国", "128MB", 75.3, "wait"],
                          ["心三国", "128MB", 80, "wait"],
                          ["心三国", "128MB", 80, "wait"],
                          ["心三国", "128MB", 80, "wait"],
                          ["心三国", "128MB", 80, "wait"],
                          ["心三国", "128MB", 80, "wait"],
                          ["心三国", "128MB", 100, "success"],
                          ["心三国", "128MB", 100, "success"],
                          ])
        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(790, 500)
    win.connect("destroy", lambda w : gtk.main_quit())
    win.add(ListView(mode_list, "theme/listview/title.png", "theme/listview/bg.png"))
    win.show_all()
    gtk.timeout_add(1500, test_modify_gui)    
    gtk.main()
    
