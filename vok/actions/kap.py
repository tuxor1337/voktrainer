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

from ..gui.dialogs import dialog_kap_add,dialog_kap_edit,dialog_kap_rem

def kap_add(win,kartei,spr):
    kap = dialog_kap_add(win)
    if kap != None:
        return kartei.add_kapitel(kap,spr)
    return None

def kap_rem(win,kartei,kap):
    if dialog_kap_rem(win):
        kartei.rem_kap(kap)
        return True
    return False

def kap_edit(win,kartei,kap):
    edited = dialog_kap_edit(win,kap[1])
    if kap[1] != edited:
        kartei.edit_kapitel(kap[0],edited)
        return edited
    return None
