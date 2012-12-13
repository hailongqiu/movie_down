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
import pangocairo
import pango

def draw_pixbuf(cr, pixbuf, x=0, y=0, alpha=1.0):
    if pixbuf != None:
        cr.set_source_pixbuf(pixbuf, x, y)
        cr.paint_with_alpha(alpha)

def get_system_font():
    font_test_window = gtk.Window(gtk.WINDOW_POPUP)
    font_test_window.set_default_size(0, 0)
    font_test_window.move(-1000000, -1000000)
    font_name = ' '.join(str(font_test_window.get_pango_context().get_font_description()).split(" ")[0:-1])
    font_test_window.destroy()    
    return font_name

DEFAULT_FONT = get_system_font()
text_size = 12

def draw_text(cr, x, y, text, color_alpha):
    context = pangocairo.CairoContext(cr)
    layout = context.create_layout()
    layout.set_font_description(pango.FontDescription("%s %s" % (DEFAULT_FONT, text_size)))
    cr.set_source_rgba(*alpha_color_hex_to_cairo(color_alpha))
    layout.set_text(text)
    (text_width, text_height) = layout.get_pixel_size()
    cr.move_to(x - text_width/2, y - text_height/2)
    context.update_layout(layout)
    context.show_layout(layout)
    return text_width, text_height
    
def alpha_color_hex_to_cairo((color, alpha)):
    (r, g, b) = color_hex_to_cairo(color)
    return (r, g, b, alpha)

def color_hex_to_cairo(color):
    gdk_color = gtk.gdk.color_parse(color)
    return (gdk_color.red / 65535.0, gdk_color.green / 65535.0, gdk_color.blue / 65535.0)
    
        
