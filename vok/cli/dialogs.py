# -*- coding: utf-8 -*-

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
   print "Führe neue Vokabel %s mit existierendem Eintrag zusammen." % (vok)
   return True
