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

class TokenInfo(object):
    def __init__(self):
        self.id   = None
        self.type = None # token type.
        self.row  = None # token row.
        
class Stack(object):
    '''
    LL(1) 语法分析.
    '''
    def __init__(self):
        self.save_values = []
    
    def pop(self):
        value = self.save_values.pop()
        return value
    
    def push(self, value):
        self.save_values.append(value)    
    

    
    
