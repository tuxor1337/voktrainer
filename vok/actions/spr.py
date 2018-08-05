# -*- coding: utf-8 -*-
#
# This file is part of Vokabeltrainer für Linux
#
# Copyright 2018 Thomas Vogt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from gi.repository import Gtk

from ..gui.dialogs import dialog_spr_edit,dialog_spr_rem,dialog_spr_add

def spr_edit(win,kartei,spr):
    response = dialog_spr_edit(win,*spr[1:4])
    if response != spr[1:4]:
        spr = [spr[0],response[0],response[1],response[2]]
        kartei.edit_sprache(*spr)
        return spr
    return None

def spr_rem(win,kartei,sprid):
    if dialog_spr_rem(win) == True:
        kartei.rem_sprache(sprid)
        return True
    return False

def spr_add(win,kartei):
    spr = dialog_spr_add(win)
    if spr != None:
        return kartei.add_sprache(spr[0],spr[1],spr[2])
    return None
