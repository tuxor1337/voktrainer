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


from sys import argv

"""dialog_kap_rem = lambda x: True
dialog_kap_edit = lambda x,y: None
dialog_kap_add = lambda x: None
dialog_spr_add = lambda x: None
dialog_spr_edit = lambda x,y,z,w: None
dialog_spr_rem = lambda x: True
dialog_vok_rem = lambda x,y: True
dialog_vok_edit = lambda x,y,z: None
dialog_vok_merge_edit = lambda x,y: None
dialog_export = lambda x: argv[2]"""
dialog_vok_merge_edit = lambda x,y: False
dialog_import = lambda x: argv[2]
def dialog_vok_merge_yn(win,vok):
   print("Führe neue Vokabel %s mit existierendem Eintrag zusammen." % (vok))
   return True
