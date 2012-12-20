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

from timer import Timer
import gobject
import subprocess        
import fcntl
import gtk
import os

DEBUG = 0
(VIDEO_TYPE, DVD_TYPE, VCD_TYPE) = range(0, 3)
(STOPING_STATE, PAUSE_STATE, STARTING_STATE)= range(0, 3)
(CHANNEL_NORMAL_STATE, CHANNEL_LEFT_STATE, CHANNEL_RIGHT_STATE ) = range(0, 3)

TYPE_NETWORK, TYPE_FILE = range(0, 2)
############################################################################
###  保存获取的信息
class Info(object):
    def __init__(self):
        self.file_name = "" # 文件名
        self.type = None # 文件类型.
        # 分辨率.
        self.width = 0 # 宽
        self.height = 0 # 高
        # 总长度.
        self.length = 0 # 媒体时长
        # 视频.
        self.video_format = None # 编码格式
        self.video_bitrate = None # 视频码率  
        self.video_fps = None # 视频帧率
        # 音频.
        self.audio_foramt = None # 编码格式.
        self.audio_bitrate = None # 音频码率
        self.audio_nch = None # 声道数.
        self.audio_rate = None # 采样数.
        # 
        self.subtitle_source = None
        self.subtitle_is_file = None
        #
        self.title_is_menu = False
        #
        self.subtitle = []
        
####################################################################        
### Mplayer后端控制.
class LDMP(gobject.GObject):
    '''Linux Deepin Mplayer 后端.'''
    __gsignals__ = {
        "get-time-pos":(gobject.SIGNAL_RUN_LAST,
                        gobject.TYPE_NONE,(gobject.TYPE_INT,)),
        "get-time-length":(gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE,(gobject.TYPE_INT, gobject.TYPE_STRING,)),
        "end-media-player":(gobject.SIGNAL_RUN_LAST,
                            gobject.TYPE_NONE,()),
        "error-msg":(gobject.SIGNAL_RUN_LAST,
                            gobject.TYPE_NONE,(gobject.TYPE_STRING,)),        
        }
    def __init__(self, xid=None):
        gobject.GObject.__init__(self)        
        # init values.
        self.init_values(xid)
        
    def init_values(self, xid):    
        self.info = None
        self.xid = xid
        self.channel_state = CHANNEL_NORMAL_STATE
        self.state = STOPING_STATE
        self.path = None
        
    def play(self, path):        
        # 保存文件路径.
        self.path = path
        # 初始化状态.
        self.state = STARTING_STATE
        # 获取播放文件信息.
        self.file_info = Info()
        #
        command = ['mplayer',
                   '-nokeepaspect',
                   '-osdlevel',
                   '0',
                   '-double',
                   '-slave',
                   '-quiet']            
        
        command.append(path)
        command.append('-wid')
        command.append('%s' % (str(self.xid)))

        self.mp_id = subprocess.Popen(command, 
                                      stdin = subprocess.PIPE,
                                      stdout = subprocess.PIPE,
                                      stderr = subprocess.PIPE,
                                      shell = False)
            
        self.mplayer_pid = self.mp_id.pid
        (self.mplayer_in, self.mplayer_out, self.mplayer_err) = (self.mp_id.stdin, self.mp_id.stdout, self.mp_id.stderr)
        fcntl.fcntl(self.mplayer_out, 
                        fcntl.F_SETFL, 
                        os.O_NONBLOCK)            
                
        # IO_HUP[Monitor the pipeline is disconnected].
        self.watch_in_id = gobject.io_add_watch(self.mplayer_out, 
                                                gobject.gobject.IO_IN, 
                                                self.player_thread_reader)
        self.watch_err_id = gobject.io_add_watch(self.mplayer_err, 
                                                 gobject.IO_IN, 
                                                 self.player_thread_reader_error)
        self.watch_in_hup_id = gobject.io_add_watch(self.mplayer_out, 
                                                    gobject.IO_HUP, 
                                                    self.player_thread_complete)
        #
        self.timer = Timer(1000)
        self.timer.connect("Tick", self.thread_query)
        self.timer.Enabled = True 
        #
        # gobject.timeout_add_seconds(1, self.thread_query, 1)        
        #
        self.get_time_length()
        # 测试输出.
        if DEBUG:
            print self.file_info.file_name
            print length_to_time(int(self.file_info.length))
            print self.file_info.video_format
            print self.file_info.video_bitrate
            print self.file_info.video_fps
            print self.file_info.audio_foramt
            print self.file_info.audio_nch
            print self.file_info.audio_bitrate
            print self.file_info.audio_rate
                        
    def thread_query(self, tick):
        self.get_time_pos()
        
    '''获取Mplayer时间.''' # t123456
    def get_percent_pos(self): # 获取当前位置为整数的百分比 
        self.cmd('get_percent_pos\n')
        # return self.get_info("ANS_PERCENT_POSITION")
            
    def get_sub_visibility(self):    
        self.cmd("get_sub_visibility\n")
        
    def get_time_length(self):    
        self.cmd('get_time_length\n')
        # return self.get_info("ANS_LENGTH")
    
    def get_time_pos(self): # 当前位置用秒表示，采用浮点数.
        self.cmd('get_time_pos\n')
        # return self.get_info("ANS_TIME_POSITION").split("\n")[0]
                                        
    def get_info(self, info_flags): # 获取返回信息.
        while True:
            try:
                line = self.mplayer_out.readline()
            except StandardError:
                break
                            
            if not line:
                break
            
            if line.strip().startswith(info_flags):
                return line.replace(info_flags, "")
            else:
                return line
            
    '''字幕控制''' # s123456
    def sub_add(self, sub_file):
        '''Load subtitle'''
        if self.state == STARTING_STATE: # STARTING_STATE
            self.cmd("sub_load '%s'\n" % (sub_file))
            
    def sub_select(self, index, drag_sub=True):        
        if self.state == STARTING_STATE: # STARTING_STATE
            self.cmd('sub_select %s\n' % str(index))
            if drag_sub:
                for sub_num in range(0, self.sub_sum):
                    self.sub_del(sub_num)

    def sub_clear(self, end_index): # clear all subtitl file.
        if self.state == STARTING_STATE:
            for index in range(0, end_index):
                self.sub_del(index)
                
    def sub_del(self, index):        
        if self.state == STARTING_STATE: # STARTING_STATE
            self.cmd('sub_remove %s\n' % index)
                        
    def sub_stop(self):        
        if self.state == STARTING_STATE:
            self.cmd("sub_select -1\n")
            
    # subtitle alignment. # 0 top 1 center 2 bottom  
    def sub_alignment_top(self):
        self.sub_alignment(0)
        
    def sub_alignment_center(self):
        self.sub_alignment(1)
        
    def sub_alignment_bottom(self):
        self.sub_alignment(2)
        
    def sub_alignment(self, alignment_state):
        if self.state == STARTING_STATE:
            self.cmd("sub_alignment %s\n"%(alignment_state))

    # subtitle delay(+/-[abs]).
    def sub_up_delay(self): # sub_delay 0.1\n sub_delay -0.1\n
        self.sub_delay(0.1)
        
    def sub_down_delay(self):
        self.sub_delay(-0.1)
    
    def sub_delay(self, value):                    
        if self.state == STARTING_STATE:
            self.cmd("sub_delay %s\n" % (value))
        
    # subtitle log.
    # def sub_log(self)
            
    # subtitle pos.    
    # def sub_pos(self)
            
    # subtitle source(source).    
    # def sub_source(self):         
            
    # subtitle file(value).        
    # def sub_file(self, value):
            
    # subtitle vob(value).        
    # def sub_vob(self, value)        
            
    # subtitle demux(value).        
    # def sub_demux(self, value):        
            
    # subtitle scale(+/-[abs])
    # sub_scale %f 1\n. 默认 1.0
    def sub_up_scale(self):
        self.subtitle_scale_value += 0.1
        self.sub_scale(self.subtitle_scale_value)
        
    def sub_down_scale(self):
        self.subtitle_scale_value -= 0.1
        self.sub_scale(self.subtitle_scale_value)
    
    def sub_scale(self, value): # value -> %f
        if self.state == STARTING_STATE:
            self.cmd("sub_scale %s 1\n" % (value));
            
    '''声音控制''' # v123456
    def addvolume(self, volume_num):
        '''Add volume'''
        self.volume = volume_num
        self.volume = min(self.volume, 100)
        
        if self.state == STARTING_STATE:
            self.cmd('volume +%s 1\n' % str(self.volume))
        
    def decvolume(self, volume_num):
        '''Decrease volume'''
        self.volume = volume_num
        self.volume = max(self.volume, 0)
        
        if self.state == STARTING_STATE:
            self.cmd('volume -%s 1\n' % str(self.volume))
            
    def setvolume(self, volume_num):
        '''Add volume'''
        self.volume = volume_num
        self.volume = max(min(self.volume, 100), 0)
        
        if self.state == STARTING_STATE:
            self.cmd('volume %s 1\n' % str(self.volume))
            
    def leftchannel(self):
        '''The left channel'''
        if self.state == STARTING_STATE:
            self.cmd('af channels=2:2:0:0:0:0\n')
            self.channel_state = CHANNEL_LEFT_STATE #1
    
    def rightchannel(self):
        '''The right channel'''
        if self.state == STARTING_STATE:
            self.cmd('af channels=2:2:0:1:1:1\n')             
            self.channel_state = CHANNEL_RIGHT_STATE #2
            
    def normalchannel(self):
        '''Normal channel'''
        if self.state == STARTING_STATE:
            self.cmd('af channels=2:2:0:0:1:1\n')
            self.channel_state = CHANNEL_NORMAL_STATE #0
            
    def offmute(self): 
        self.volumebool = False
        self.cmd('mute 0\n')
                
    def nomute(self):
        '''Active mute'''
        self.volumebool = True
        self.cmd('mute 1\n')
                
    def off_switch_audio(self):
        self.switch_audio(-1)
        
    def switch_audio(self, number):        
        self.cmd('switch_audio %s\n'% str(number))
        self.aid_number = number
            
    '''视频控制''' # video123456
    # brightness.
    def addbri(self, bri_num):
        '''Add brightness'''
        if self.state == STARTING_STATE:
            self.cmd('brightness +%s\n' % (bri_num))
    
    def decbri(self, bri_num):
        '''Decrease brightness'''
        if self.state == STARTING_STATE:
            self.cmd('brightness -%s\n' % (bri_num))
    
    # saturation.
    def addsat(self, sat_num):
        '''Add saturation'''
        if self.state == STARTING_STATE:
            self.cmd('saturation +%s\n' % (sat_num))
            
    def decsat(self, sat_num):
        '''Decrease saturation'''        
        if self.state == STARTING_STATE:
            self.cmd('saturation -%s\n' % (sat_num))
    
    # contrast. 
    def addcon(self, con_num):
        '''Add contrast'''
        if self.state == STARTING_STATE:
            self.cmd('contrast +%s\n' % (con_num))    
            
    def deccon(self, con_num):
        '''Decrease contrast'''    
        if self.state == STARTING_STATE:
            self.cmd('contrast -%s\n' % (con_num))
    
    # hue.
    def addhue(self, hue_num):
        '''Add hue'''
        if self.state == STARTING_STATE:
            self.cmd('hue +%s\n' % (hue_num))        
    def dechue(self, hue_num):
        '''Decrease hue'''
        if self.state == STARTING_STATE:
            self.cmd('hue -%s\n' % (hue_num))
        
    '''dvd控制''' #dvd123456
    # cdrom [dvd, vcd, cd].        
    def dvd_mouse_pos(self, x, y):        
        if self.state == STARTING_STATE:
            self.cmd('set_mouse_pos %d %d\n' % (int(x), int(y)))
        
    def dvd_up(self):
        self.cmd('dvdnav up\n')
        
    def dvd_down(self):    
        self.cmd('dvdnav down\n')
            
    def dvd_left(self):        
        self.cmd('dvdnav left\n')
        
    def dvd_right(self):
        self.cmd('dvdnav right\n')
        
    def dvd_menu(self):    
        self.cmd('dvdnav menu\n')
        
    def dvd_select(self):
        self.cmd("dvdnav select\n")
    
    def dvd_prev(self):    
        self.cmd("dvdnav prev\n")
        
    def dvd_mouse(self):    
        if self.state == STARTING_STATE:
            self.cmd('dvdnav mouse\n')
        
    def switch_angle(self, value):    
        self.cmd("switch_angle '%s'\n" % (value))
        
    def next_title(self, value):    
        self.switch_title(value)
        
    def prev_title(self, value):    
        self.switch_title(value)
        
    def switch_title(self, value):
        self.cmd("switch_title %d\n" % (int(value)))
        
    def switch_chaptet(self, value, type_):
        self.cmd("switch_chaptet '%s' '%s'" % (value, type_))
            
    '''播放器控制[快进，倒退，暂停]'''    
    def seek(self, seek_num):        
        '''Set rate of progress'''
        if self.state == STARTING_STATE:
            self.cmd('seek %d 2\n' % (seek_num))               
            
    def fseek(self, seek_num):
        '''Fast forward'''
        if self.state == STARTING_STATE or self.state == PAUSE_STATE:
            self.cmd('seek +%d\n' % (seek_num))   
            
    def bseek(self, seek_num):
        '''backward'''
        if self.state == STARTING_STATE or self.state == PAUSE_STATE:
            self.cmd('seek -%d\n' % (seek_num))
            
    def pause(self, pause_dvd=False):
        if (self.state == STARTING_STATE or self.state == PAUSE_STATE):
            if self.state == PAUSE_STATE:
                self.state = STARTING_STATE
            else:    
                self.state = PAUSE_STATE
            self.cmd('pause \n')
        
    '''截图'''
    # def screenshot(self, value=0):
    #    self.cmd("screenshot %d /home/long \n" % (value))
    
    def screenshot(self, path=None, outdir=".", type="jpeg"):
        if not path:
            path = self.path
        os.system("mplayer -ss 1 -noframedrop -nosound -vo %s:outdir=%s -frames 1 %s >/dev/null 2>&1" % (type, outdir, path))
        
    '''给Mplayer发送命令''' #cmd123456
    def cmd(self, cmd_str):
        '''Mplayer command'''
        try:            
            self.mplayer_in.write(str(cmd_str))
            self.mplayer_in.flush()
        except StandardError, e:
            if DEBUG:
                print 'command error %s' % (e)            

    '''mplayer 管道控制'''
    def player_thread_reader(self, source, condition):    
        if source == None:
            return False        
        
        # if self.player_state == PLAYER_STATE_DEAD
        
        buffer = source.readline()
        if buffer == gobject.IO_STATUS_ERROR:
            if DEBUG:
                print "GIO IO Error:", buffer
            return True
        else:
            if DEBUG:
                if buffer.find("ANS") == None:
                    print buffer
            #        
            #
            # if buffer.startswith("Cache fill")
                # percent = buffer.replace("Cache fill:")
            #    
            # if buffer.startswith("AO:") != None:
                # self.cmd("get_property switch_audio\n")
            # if buffer.startswith("VO:")    
                # self.file_info.width
                # self.file_info.height 
            # if buffer.startswith("Video: no video"):
                # self.file_info.width = 0
                # self.file_info.height = 0
            # 
            if buffer.startswith("ANS_TIME_POSITION"):
                pos =  float(buffer.replace("ANS_TIME_POSITION=", "").split("\n")[0])
                if pos >= 0:
                    self.emit("get-time-pos", pos)
                if pos > self.file_info.length: # 结束播放.
                    self.quit()
            #   
            if buffer.startswith("ID_START_TIME"):
                print buffer.replace("ID_START_TIME=", "")
            #    
            if buffer.startswith("ID_LENGTH"):
                print buffer.replace("ID_LENGTH=", "")
            #    
            if buffer.startswith("ANS_LENGTH"):
                length = float(buffer.replace("ANS_LENGTH=", "").split("\n")[0])
                self.file_info.length = length
            #    
            if buffer.startswith("ID_AUDIO_TRACK"):
                print buffer.replace("ID_AUDIO_TRACK=", "")
                
            if buffer.startswith("ANS_switch_audio"):               
                print buffer.replace("ANS_switch_audio=", "")
               
            if buffer.startswith("ANS_sub_source"):    
                self.file_info.subtitle_source = buffer.replace("ANS_sub_source")
                if self.file_info.subtitle_source == 0:
                    self.file_info.subtitle_is_file = True
                    self.cmd("get_property sub_file\n")
                elif self.file_info.subtitle_source == 1:    
                    self.file_info.subtitle_is_file = False
                    self.cmd("get_property sub_vob\n")
                elif self.file_info.subtitle_source == 2:
                    self.file_info.subtitle_is_filew = False
                    self.cmd("get_property sub_demux\n")
                                        
            if buffer.startswith("ANS_sub_file"):
                print buffer.replace("ANS_sub_file", "")
                
            if buffer.startswith("ANS_sub_demux"):    
                print buffer.replace("ANS_sub_demux", "")
                
            if buffer.startswith("DVDNAV_TITLE_IS_MENU"):
                self.file_info.title_is_menu = True
                self.get_time_length()
                
            if buffer.startswith("DVDNAV_TITLE_IS_MOVIE"): 
                self.file_info.title_is_menu = False
                self.get_time_length()
                
            if buffer.startswith("ID_SUBTITLE_ID="): 
                print buffer
                id = buffer.replace("ID_SUBTITLE_ID=", "")
                lang = buffer.startswith("Unknown")
                name =buffer.startswith("Unknown")
                subtitle_tuple = (name, lang, id)
                self.file_info.subtitle.append(subtitle_tuple)
                
                
            if buffer.startswith("ID_SID_"):
                print buffer
                id = buffer.replace("ID_SID_", "")
                # buffer.readline()
                # if buffer.startswith("_LANG="):                    
                # ... ...
                    
            if buffer.startswith("ID_FILE_SUB_ID="):
                print buffer
                id = buffer.replace("ID_FILE_SUB_ID=")
                # ... ...
                
            if buffer.startswith("ID_AUDIO_ID="):    
                print buffer
                id = buffer.replace("ID_AUDIO_ID=", "")
                # ... ...
                
            if buffer.startswith("ID_AID_"):    
                print buffer
                id = buffer.replace("ID_AID_", "")
                # _NAME=" ... ... _LANG=
                
            if  buffer.startswith("ID_CHAPTERS="):   
                print buffer.replace("ID_CHAPTERS=", "")
                
            if (buffer.startswith("ID_SEEKABLE=")
                and buffer.startswith("ID_SEEKABLE=0")):    
                print buffer
                print "True"
                
            if buffer.startswith("ID_VIDEO_FORMAT"):
                print buffer
                # buffer.startswith("ID_VIDEO_FORMAT")
                # len("ID_VIDEO_FORMAT=")
                # self.file_info.width == 0 and self.file_info.height == 0
                
            if buffer.startswith("ID_VIDEO_CODEC"):
                print buffer
                # len("ID_VIDEO_CODEC=")
                
            if buffer.startswith("ID_VIDEO_FPS"):    
                print buffer.replace("ID_VIDEO_FPS=", "")
                
            if buffer.startswith("ID_VIDEO_BITRATE"):    
                print buffer.replace("ID_VIDEO_BITRATE=", "")
                
            #    
            if buffer.startswith("ID_AUDIO_FORMAT"):
                print buffer
                # len("ID_AUDIO_FORMAT=")
                #... ...
            if buffer.startswith("ID_AUDIO_CODEC"):
                print buffer
                # len("ID_AUDIO_CODEC=")
                # ... ...
            if buffer.startswith("ID_AUDIO_BITRATE"):    
                print buffer.replace("ID_AUDIO_BITRATE=", "")
                
            if buffer.startswith("ID_AUDIO_RATE"):    
                print buffer.replace("ID_AUDIO_RATE=", "")
            if buffer.startswith("ID_AUDIO_NCH"):    
                print buffer.replace("ID_AUDIO_NCH=", "")
                
                
            if buffer.startswith("*** screenshot"):    
                #... ...
                print buffer
            
            if buffer.startswith("Name   : "):
                print buffer
                
            if buffer.startswith("Genre  : "):
                print buffer
                
            if buffer.startswith("Title: "):    
                print buffer
                
            if buffer.startswith("Artist: "):    
                print buffer
                
            if buffer.startswith("Album: "):    
                print buffer
                
            # minimum_mplayer == False    
                
            if buffer.startswith("ICY Info"):
                print buffer
                # ... ...
                
            if buffer.startswith("ID_FILENAME"):   
                print buffer
                # ... ...
                
                
                
                
        return True
    
    def player_thread_reader_error(self, source, condition):
        error_msg = None
        if source == None:
            remove_timeout_id(self.watch_in_hup_id)
            remove_timeout_id(self.watch_in_id)            
            return False
        try:
            buffer = source.readline()
        except Exception , e:
            error_msg = e            
            buffer = ""
            
        if DEBUG:    
            if buffer.startswith("ANS") == None:
                print "error: ", buffer
            
        if buffer.startswith("Couldn't open DVD device") != 0:
            error_msg = buffer
            
        if buffer.startswith("X11 error") != 0:    
            error_msg = buffer
        
        if buffer.startswith("signal") != None:
            error_msg = buffer
        
        # if buffer.startswith("Failed creating VDPAU decoder"):
            
        # if buffer.startswith("decoding to PIX_FMT_NONE is not supported"):
            
        if buffer.find("Failed to open") != -1:    
            if (buffer.find("LITC") == -1 
                and buffer.find("/dev/rtc") == -1 
                and buffer.find("VDPAU") == -1 
                and buffer.find("registry file") == -1):
                # 
                if (buffer.find("<") == -1 
                    and buffer.find(">") == -1 
                    and self.file_info.type == TYPE_FILE):
                    error_msg = ""
                # mms error.
                if buffer.find("mms://") != -1 and self.file_info.type == TYPE_NETWORK:
                    pass
                   
        if buffer.find("No stream found to handle url mmshttp://") != -1:
            pass
        
        if (buffer.find("Server returned 404:File Not Found") != -1 
            and buffer.find("mmshttp://") != -1):
            pass
        
        if (buffer.find("unknown ASF streaming type") != -1 
            and buffer.find("mmshttp://")):
            pass
        
        if buffer.find("Error while parsing chunk header") != -1:
            pass
        
        if buffer.find('Failed to initiate \"video/X-ASF-PF\" RTP subsession') != -1:
            pass
        
        if buffer.find("Playlist support will not be used") != -1:
            pass
        
        if buffer.find("Compressed SWF format not supported") != -1:
            pass
        
        if buffer.find("moov atom not found") != -1:
            pass

        if buffer.find("MOV: missing header (moov/cmov) chunk") != -1:
            pass

        if buffer.find("Seek failed") != -1:
            pass
        
        if buffer.find("Title: ") != 0:
            pass
                    
        if error_msg != None:
            self.emit("error-msg", error_msg)
            
        return True
    
    def player_thread_complete(self, source, condition): 
        if DEBUG:
            print "player_thread_complete:", "断开管道!!"
        try:
            # modify state.
            self.state = STOPING_STATE
            # close fd.
            self.mplayer_in.close()
            self.mplayer_out.close()
            self.mplayer_err.close()
            # kill mplayer.
            self.mp_id.kill() 
            os.system("kill %s" % (self.mplayer_pid)) # 杀死 mplayer pid.
            self.timer.Enabled = False # 关闭发送get-time-pos命令的时钟.            
            self.emit("end-media-player")
        except StandardError, e:
            print "player_thread_complete:", e
        return False
    
    def quit(self): # 退出.
        self.cmd('quit \n')       
                
def remove_timeout_id(callback_id):
    if callback_id:
        gobject.source_remove(callback_id)
        callback_id = None
                                               
########################################################                
## 转换时间的函数.                
def length_to_time(length):  
    time_sec = int(float(length))
    time_hour = 0
    time_min = 0
    
    if time_sec >= 3600:
        time_hour = int(time_sec / 3600)
        time_sec -= int(time_hour * 3600)
        
    if time_sec >= 60:
        time_min = int(time_sec / 60)
        time_sec -= int(time_min * 60)         
        
    return str("%s:%s:%s"%(str(time_add_zero(time_hour)), 
                           str(time_add_zero(time_min)), 
                           str(time_add_zero(time_sec))))
                
def time_add_zero(time_to):    
    if 0 <= time_to <= 9:
        time_to = "0" + str(time_to)
    return str(time_to)
        

############################################################
### 画面比例

ASCEPT_4X3_STATE = "4:3"
ASCEPT_16X9_STATE = "16:9"
ASCEPT_16X10_STATE = "16:10"
ASCEPT_1_85X1_STATE = "1.85:1" 
ASCEPT_2_35X1_STATE = "2.35:1"

def set_ascept_function(screen_frame, video_aspect):
    x, y, w, h = screen_frame.allocation
    screen_frame_aspect = round(float(w) / h, 2)
    #
    if screen_frame_aspect == video_aspect:
        screen_frame.set(0.0, 0.0, 1.0, 1.0)
    elif screen_frame_aspect > video_aspect:
        x = (float(h)* video_aspect) / w
        if x > 0.0:
            screen_frame.set(0.5, 0.0, max(x, 0.1, 1.0), 1.0)
        else:
            screen_frame.set(0.5, 0.0, 1.0, 1.0)
    elif screen_frame_aspect < video_aspect:
        y = (float(w) / video_aspect) / h;
        if y > 0.0:
            screen_frame.set(0.0, 0.5, 1.0, max(y, 0.1, 1.0))
        else:
            screen_frame.set(0.0, 0.5, 1.0, 1.0)

def max(x, low, high):
    if low <= x <= high:
        return x
    if low > x:
        return low
    if high < x:
        return high
    
# 获取播放窗口的XID.
def get_window_xid(widget):
    return widget.window.xid
    
'''关闭和打开双缓冲.'''
def unset_flags(screen):
    '''Set double buffer.'''
    screen.unset_flags(gtk.DOUBLE_BUFFERED)

def set_flags(screen):
    '''Set double buffer.'''
    screen.set_flags(gtk.DOUBLE_BUFFERED)

#########################################################    
## test.    
if __name__ == "__main__":            
    def get_time_pos_test(mp, pos):
        print "pos:", pos
        pb_btn.set_label(str(pos))
        
    def get_time_length_test(mp, length, time):    
        print "length:", length, "time:", time
        
    def modify_ascept(widget, event):
        if mp.state == STARTING_STATE:
            set_ascept_function(screen_frame, 4.0/3.0)
        
    def pause_clicked(widget):    
        mp.pause()
        
    def fseek_btn_clicked(widget):    
        mp.fseek(50)
        
    def draw_screen(widget, event):    
        cr = widget.window.cairo_create()
        rect = widget.allocation
        cr.rectangle(rect.x, rect.y, rect.width, rect.height)
        cr.fill()
        
    def quit_window(widget):    
        mp.quit()
        gtk.main_quit()        
        
    def end_media_player(mp):    
        print '播放结束了'
        # mp.play("../../../../../test.rmvb")
        set_flags(screen)
        screen_frame.set(0.0, 0.0, 1.0, 1.0)
        
    def rect_error_msg(mp, msg):
        print "error_msg:", msg
        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(300, 300)
    vbox = gtk.VBox()
    screen_frame = gtk.Alignment()
    screen_frame.connect("expose-event", draw_screen)
    screen_frame.set(0, 0, 1, 1)
    screen = gtk.DrawingArea()
    screen_frame.add(screen)    
    screen.set_has_window(True)
    screen.set_can_focus(True)
    screen.set_can_default(True)
    unset_flags(screen)
    screen.activate()    
    pb_btn = gtk.Button("进度条")
    
    hbox = gtk.HBox()
    pause_btn = gtk.Button("暂停")
    fseek_btn = gtk.Button("快进")
    pause_btn.connect("clicked", pause_clicked)
    fseek_btn.connect("clicked", fseek_btn_clicked)
    hbox.pack_start(pause_btn, False, False)
    hbox.pack_start(fseek_btn, False, False)
    
    vbox.pack_start(screen_frame, True, True)
    vbox.pack_start(pb_btn, False, False)
    vbox.pack_start(hbox, False, False)
    
    win.add(vbox)
    win.connect("destroy", quit_window)
    win.connect("configure-event", modify_ascept)
    win.connect("check-resize", modify_ascept, 1)
    win.show_all()
    vbox.show_all()
    #
    mp = LDMP(get_window_xid(screen))
    mp.play("../../../test.rmvb")
    # mp.play("../../../123.mp3")
    mp.connect("get-time-pos", get_time_pos_test)    
    mp.connect("get-time-length", get_time_length_test)    
    mp.connect("end-media-player", end_media_player)
    mp.connect("error-msg", rect_error_msg)
    gtk.main()
