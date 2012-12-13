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

import pygame

class  Sound(object):
    def __init__(self):                
        self.pause = False
        
    def play(self, path):            
        pygame.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        
    def pause(self):    
        if self.pause:
            pygame.mixer.music.unpause()
        else:    
            pygame.mixer.music.pause()
        self.pause = not self.pause
        
    def stop(self):    
        pygame.mixer.music.stop()
        
    def fadeout(self, time):    
        pygame.mixer.music.fadeout(time)
        
    def set_volume(self, value):    
        pygame.mixer.music.set_volume(value)
        
    def get_pos(self):    
        return pygame.mixer.music.get_pos()
    
sound_play = Sound()    

if __name__ == "__main__":    
    sound = Sound()
    sound.play("test.wav")
    import gtk
    gtk.main()
'''
Sound对象：
方法名 	作用
fadeout 	淡出声音，可接受一个数字（毫秒）作为淡出时间
get_length 	获得声音文件长度，以秒计
get_num_channels 	声音要播放多少次
get_volume 	获取音量（0.0 ~ 1.0）
play 	开始播放，返回一个Channel对象，失败则返回None
set_volume 	设置音量
stop 	立刻停止播放
'''
