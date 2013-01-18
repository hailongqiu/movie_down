#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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


from utils import get_home_path
import os
import sys


class PluginManage(object):
    def __init__(self, sys_path=os.path.join(get_home_path(), ".config/deepin-media-player")):        
        init_file = os.path.join(get_home_path(), ".config/deepin-media-player/ldmp_plugins/__init__.py")
        ldmp_plugins_path = os.path.join(get_home_path(), ".config/deepin-media-player/ldmp_plugins")
        if not os.path.exists(ldmp_plugins_path):
            os.makedirs(ldmp_plugins_path)
        if not os.path.exists(init_file):            
            init_file_fd = open(init_file, "w")
            init_file_fd.close()
        ################################    
        self.active_sys_path(sys_path)
        self.plugins_list = []
        self.plugins_dict = {}
        # self.load_dir(sys_path)
        
    def load_dir(self, plugin_path=os.path.join(get_home_path(), ".config/deepin-media-player")):
            if os.path.exists(os.path.join(plugin_path, "ldmp_plugins")):
                self.active_sys_path(plugin_path)
                for filename in os.listdir(os.path.join(plugin_path, "ldmp_plugins")):
                    if plugins_check(filename):
                        continue
                    self.add_file(filename)
            else:  
                print "load_dir[error]: plugin path(%s) no exists" % (plugin_path)
                        
    def add_file(self, filename):
        try:
            plugin_name = os.path.splitext(filename)[0]
            plugin = __import__("ldmp_plugins." + plugin_name, 
                            fromlist=[plugin_name])
            clazz = plugin.return_plugin()
            o =clazz()
            if not self.plugins_dict.has_key(o.name()):
                if o.insert() != None:
                    self.plugins_list.insert(int(o.insert()), o)
                else:    
                    self.plugins_list.append(o)
                self.plugins_dict[o.name()] = o
                return o
            else:
                # print "%s有相同的插件名字:%s" % (plugin_name, o.name())
                return None
        except Exception, e:    
            print "add_file-->%s[error plugin]:%s" % (filename, e)
            return None
            
    def load_zip(self, zip_path, install_path=os.path.join(get_home_path(), ".config/deepin-media-player/ldmp_plugins")):
        for filename in install_zip_plugin(zip_path, install_path):            
                return self.add_file(filename)
        
    def active_sys_path(self, plugin_path):
        if plugin_path not in sys.path:
            sys.path.append(plugin_path)
        
    def clear(self):
        for o in self.plugins_list:
            o.stop()
            o.setPlatform(None, None, None)
        self.plugins=[]
        

def plugins_check(filename):        
    if (not filename.endswith(".py") 
        or filename.startswith("_") 
        or filename.startswith(".#")):
        return True
    else:
        return False
    
'''用于导入zip格式的插件'''
import zipfile

def install_zip_plugin(filename, install_path):
    with zipfile.ZipFile(filename) as pluginzip:        
        pluginzip.extractall(install_path)
        return pluginzip.namelist()
