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

import subprocess
import gtk

class  Sound(object):
    def __init__(self):        
        pass
        
    def play(self, path, time=None):            
        self.path = path
        command = ['mplayer']
        command.append(path)
        
        self.sound_id = subprocess.Popen(command, 
                                      stdin = subprocess.PIPE,
                                      stdout = subprocess.PIPE,
                                      stderr = subprocess.PIPE,
                                      shell = False)                
        #
        (self.sound_in, self.sound_out) = (self.sound_id.stdin, self.sound_id.stdout)
        #
        if time != None:
            gtk.timeout_add(int(time * 1000), self.close_sound_time)
        
    def close_sound_time(self):    
        self.sound_in.close()
        self.sound_out.close()
        self.sound_id.kill()
        
if __name__ == "__main__":        
    sound = Sound()
    sound.play('test.mp3')
    gtk.main()
