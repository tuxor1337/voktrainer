# -*- coding: utf-8 -*-

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
