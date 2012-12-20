#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
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



import random



'''播放列表: 
       0        1       2         3          4
   { 单曲播放、顺序播放、随机播放、单曲循环播放、列表循环播放、}
'''


SINGLA_PLAY, ORDER_PLAY, RANDOM_PLAY, SINGLE_LOOP, LIST_LOOP = range(0, 5)

class PlayList(object):
    def __init__(self):
        self.__state = ORDER_PLAY # 默认顺序播放
        self.__file_list = []
        self.__current_file = None
        self.__index = -1
        
    def delete(self, play_file): # 删除文件.
        self.__file_list.remove(play_file)
        
    def append(self, play_file): # 添加文件
        self.__file_list.append(play_file)
        
    def clear(self): # 清空播放列表
        self.__file_list = []
        
    def insert(self, index, play_file):    
        self.__file_list.insert(index, play_file)
        
    def set_state(self, state):    
        self.__state = state
        
    def get_next_file(self): # 获取下一个播放文件
        if self.__file_list:
            if self.__state == SINGLA_PLAY:
                return self.__singla_play()
            elif self.__state == ORDER_PLAY:
                return self.__order_play()
            elif self.__state == RANDOM_PLAY:    
                return self.__random_play()
            elif self.__state == SINGLE_LOOP:
                return self.__single_loop_play()
            elif self.__state == LIST_LOOP:
                return self.__list_loop_play()
        else:    
            return False
        
    def print_file_list(self): # 获取当前播放文件        
        for file_ in self.__file_list:
            print "playlist:", file_
                    
    def __singla_play(self): # 单曲播放
        return False
    
    def __order_play(self): # 顺序播放
        if self.__index + 1 > len(self.__file_list) - 1:
            return False
        self.__index += 1
        return self.__file_list[self.__index]
            
    def __random_play(self): # 随机播放
        index = random.randint(0, len(self.__file_list)-1)
        self.__index = index
        return self.__file_list[index]
    
    def __single_loop_play(self): # 单曲循环播放
        return self.__file_list[self.__index]
    
    def __list_loop_play(self): # 列表循环播放
        self.__index += 1
        self.__index = self.__index % (len(self.__file_list)) 
        return self.__file_list[self.__index]
    
    def set_index(self, play_file): # 设置index.
        self.__index = self.__file_list.index(play_file)
        
    
if __name__ == "__main__":    
    play_list = PlayList()
    # play_list.set_state(SINGLA_PLAY)
    # play_list.set_state(ORDER_PLAY)
    play_list.set_state(RANDOM_PLAY)
    play_list.append("/home/long/123.rmvb")
    play_list.append("/home/long/123.rmvb123")
    play_list.append("/home/long/123.rmvb134")
    play_list.append("/home/longfdjsfj/123.rmvb134")
    play_list.append("/home房间打扫房间/longfdjsfj/123.rmvb134")
    #############################################################
    play_list.set_index("/home/longfdjsfj/123.rmvb134") 
    # play_list.delete("/home/long/123.rmvb")
    ####################
    play_list.print_file_list()
    file = play_list.get_next_file()
    if file:
       print "file:", file
    ##########################   
    play_list.set_state(ORDER_PLAY)   
    file = play_list.get_next_file()
    if file:
       print "file:", file
    ##########################   
    play_list.set_state(SINGLE_LOOP)   
    file = play_list.get_next_file()
    if file:
       print "file:", file
    ##########################   
    play_list.set_state(LIST_LOOP)   
    file = play_list.get_next_file()
    if file:
       print "file:", file
        
