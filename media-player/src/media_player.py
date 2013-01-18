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



from skin import app_theme
from dtk.ui.draw import draw_pixbuf
from dtk.ui.utils import color_hex_to_cairo
from locales import _ # 国际化翻译.
from utils import get_home_path
from plugin_manage import PluginManage
from gui import GUI # 播放器界面布局.
import gtk
import sys
import os
# mplayer后端.
from mplayer.player import LDMP, set_ascept_function, unset_flags, set_flags
from mplayer.player import ASCEPT_4X3_STATE, ASCEPT_16X9_STATE, ASCEPT_5X4_STATE
from mplayer.player import ASCEPT_16X10_STATE, ASCEPT_1_85X1_STATE, ASCEPT_2_35X1_STATE, ASCEPT_FULL_STATE, ASCEPT_DEFULAT
from mplayer.player import (ERROR_RETRY_WITH_MMSHTTP, ERROR_RESOLVE_AF_INET, ERROR_SOCKET_CONNECT,
                            ERROR_FILE_FORMAT, ERROR_DVD_DEVICE, ERROR_RETRY_ALSA_BUSY,
                            ERROR_RETRY_WITH_HTTP, ERROR_RETRY_WITH_HTTP_AND_PLAYLIST,
                            ERROR_RETRY_WITH_PLAYLIST)
from mplayer.player import TYPE_FILE, TYPE_CD, TYPE_DVD, TYPE_VCD, TYPE_NETWORK, TYPE_DVB, TYPE_TV
from mplayer.playlist import PlayList, SINGLA_PLAY, ORDER_PLAY, RANDOM_PLAY, SINGLE_LOOP, LIST_LOOP 
# 播放列表 .       0        1       2         3          4
#           { 单曲播放、顺序播放、随机播放、单曲循环播放、列表循环播放、}
#            SINGLA_PLAY ... ...                ...LIST_LOOP

class MediaPlayer(object):
    def __init__(self):
        self.plugin_manage = PluginManage()
        self.gui = GUI()        
        self.play_list = PlayList() 
        # self.play_list.set_state(SINGLA_PLAY)
        # test play list.
        # self.play_list.append("http://start.linuxdeepin.com/zh_CN/")
        # self.play_list.append("file:///home/long/Desktop/test/123.mp3")
        self.play_list.append("/home/long/Desktop/test/test.rmvb")
        self.play_list.append("http://www.baidu.com")
        self.play_list.append("http://f.youku.com/player/getFlvPath/sid/00_00/st/flv/fileid/030002010050D71213AC2A0109ACBF094EBA1F-15ED-793A-6F35-38A14136D34B?K=e14522dc10e3905d261cbe85")
        self.play_list.append("/home/long/Desktop/test/弃宝之岛-遥与魔法镜.mp4")
        # self.play_list.append("/home/long/Desktop/test/(www.kk16.com)人再囧途之泰囧_TS抢先版国语.rmvb")
        # self.play_list.append("/home/long/Desktop/test/渡边危机（上layp）HD.mp4")
        # self.play_list.append("/home/long/Desktop/test/王的盛宴TC[www.il168.com].rmvb")
        
        self.argv_path_list = sys.argv # save command argv.        
        
        '''application events init.'''
        self.gui.app.titlebar.min_button.connect("clicked", self.app_window_min_button_clicked)        
        self.gui.app.window.connect("destroy", self.app_window_quit)
        self.gui.app.window.connect("configure-event", self.app_window_configure_event)
        self.gui.app.window.connect("check-resize", self.app_window_check_resize)
        # self.app.window.connect("window-state-event", )
        # self.app.window.connect("leave-notify-event", )
        # self.app.window.connect("focus-out-event", )
        # self.app.window.connect("focus-in-event", )
        # self.app.window.connect("key-press-event", )
        # self.app.window.connect("key-release-event", )
        # self.app.window.connect("scroll_event", )
        # self.app.window.connect("check-resize",)         
                
        '''screen events init.'''
        self.draw_check = True
        self.background = app_theme.get_pixbuf("player.png").get_pixbuf()        
        self.gui.screen.connect("realize", self.init_media_player)
        self.gui.screen.connect("expose-event", self.screen_expose_event)
        self.gui.screen_frame.connect("expose-event", self.screen_frame_expose_event)
        
        # show gui window.
        self.gui.app.window.show_all()
                
    '''初始化插件系统'''    
    def init_plugin_manage(self):
        # 加载自带插件.
        for zip_file in os.listdir("plugins"):
            try:
                self.plugin_manage.load_zip(os.path.join("plugins", zip_file))
            except Exception, e:        
                print "init_plugin_manage[error]:", e
                
        # 加载用户编写的插件.
        self.plugin_manage.load_dir()
        
        for plugin in self.plugin_manage.plugins_list:
            # if not plugin.name() in zip_name_list:
            if plugin.auto():
                plugin.init_values(self, self.gui, self.ldmp)
                plugin.start()
        
    '''application event conect function.窗口事件连接函数.'''
    def app_window_min_button_clicked(self, widget): # 缩小按钮单击.
        print "app_window_min_button_clicked function", "-->>min window!!"
        
    def app_window_quit(self, widget): # 窗口销毁.destroy
        self.ldmp.quit()
        # print "app_window_quit function", "window quit!!"
        
    def app_window_configure_event(self, widget, event): # configure-event
        self.set_ascept_restart() # 设置分辨率.
        
    def app_window_check_resize(self, widget):# check-resize    
        self.set_ascept_restart() # 设置分辨率.
        
    def set_ascept_restart(self):    
        try:            
            unset_flags(self.gui.screen)
            if self.ldmp.player.video_width == 0 or self.ldmp.player.video_height == 0:
                set_flags(self.gui.screen)
                ascept_num = None
            elif self.ldmp.player.ascept_state == ASCEPT_4X3_STATE:
                ascept_num = 4.0/3.0
            elif self.ldmp.player.ascept_state == ASCEPT_16X9_STATE:    
                ascept_num = 16.0/9.0
            elif self.ldmp.player.ascept_state == ASCEPT_16X10_STATE:    
                ascept_num = 16.0/10.0
            elif self.ldmp.player.ascept_state == ASCEPT_1_85X1_STATE:    
                ascept_num = 1.85/1.0
            elif self.ldmp.player.ascept_state == ASCEPT_5X4_STATE:    
                ascept_num = 5.0/4.0
            elif self.ldmp.player.ascept_state == ASCEPT_2_35X1_STATE:    
                ascept_num = 2.35/1.0
            elif self.ldmp.player.ascept_state == ASCEPT_FULL_STATE:
                ascept_num = None
            elif self.ldmp.player.ascept_state == ASCEPT_DEFULAT:
                ascept_num = self.ldmp.player.video_width / self.ldmp.player.video_height
            else:
                ascept_num = None
                set_flags(self.gui.screen)
            # set ascept.    
            set_ascept_function(self.gui.screen_frame, ascept_num)
        except Exception, e:
            set_ascept_function(self.gui.screen_frame, None)
            print "set_ascept_restart[error]:", e
                    
            
    '''screen event conect function.播放屏幕事件连接函数'''
    def screen_frame_expose_event(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(rect.x, rect.y, rect.width, rect.height)
        cr.fill()
        
    def init_media_player(self, widget): # screen realize.        
        '''初始化mplayer后端'''
        self.ldmp = LDMP(widget.window.xid)
        
        self.ldmp.connect("get-time-pos", self.ldmp_get_time_pos)
        self.ldmp.connect("get-time-length", self.ldmp_get_time_length)
        self.ldmp.connect("end-media-player", self.ldmp_end_media_player)
        self.ldmp.connect("start-media-player", self.ldmp_start_media_player)
        self.ldmp.connect("screen-changed", self.ldmp_screen_changed)
        self.ldmp.connect("error-msg", self.ldmp_error_msg)
        
        # self.ldmp.player.ascept_state = ASCEPT_16X10_STATE
        # self.ldmp.player.vo = "vdpau"
        self.ldmp.player.type = TYPE_NETWORK
        # self.ldmp.player.ascept_state = ASCEPT_4X3_STATE
        # self.ldmp.player.uri = "/home/long/Desktop/test/123.mp3"        
        # self.ldmp.play()                
        # 初始化插件系统.
        self.init_plugin_manage()
        
    def ldmp_get_time_pos(self, ldmp, pos, time):
        # print "pos:", pos
        pass
        
    def ldmp_get_time_length(self, ldmp, length, time):    
        # print "length:", length, time
        pass
        
    def ldmp_start_media_player(self, ldmp):    
        print "开始播放了..."
        self.player_start_init()
        
    def player_start_init(self):    
        pass
    
    def ldmp_end_media_player(self, ldmp):
        print "播放结束!!", ldmp.player.type
        self.player_end_init()
        
    def player_end_init(self):        
        self.ldmp.player.video_width = 0
        self.ldmp.player.video_height = 0
        self.set_draw_background(0, 0)
        
    def ldmp_screen_changed(self, ldmp, video_width, video_height):
        self.set_draw_background(video_width, video_height) # 是否画播放器屏幕显示的背景.
        
    def set_draw_background(self, video_width, video_height):
        if video_width == 0 or video_height == 0:            
            self.draw_check = True
        else:
            self.draw_check = False
        self.set_ascept_restart() # 改变屏幕比例.    
        
    def ldmp_error_msg(self, ldmp, error_code):
        print "ldmp_error_msg->error_code:", error_code
        
    def screen_expose_event(self, widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        if self.draw_check: # 是否画播放器屏幕显示的背景.
            cr.set_source_rgb(*color_hex_to_cairo("#0D0D0D")) # 1f1f1f
            cr.rectangle(rect.x-2, rect.y-26, rect.width, rect.height)
            cr.fill()
            draw_pixbuf(cr,
                        self.background, 
                        rect.x + rect.width/2 - self.background.get_width()/2, 
                        rect.y + rect.height/2 - self.background.get_height()/2 - 26)
                        
    '''plug-in-->Public function inf.插件-->函数接口'''    
    # 上一曲.
    def prev(self):    
        play_file = self.play_list.get_prev_file()
        if play_file:
            self.ldmp.quit()
            gtk.timeout_add(88, self.timeout_prev, play_file)
            
    def timeout_prev(self, play_file):
        self.ldmp.player.uri = play_file
        self.ldmp.play()
    
    # 下一曲.
    def next(self):    
        play_file = self.play_list.get_next_file()
        if play_file:
            self.ldmp.quit()
            gtk.timeout_add(88, self.timeout_next, play_file)
        
    def timeout_next(self, play_file):        
        self.ldmp.player.uri = play_file
        self.ldmp.play()                
        
