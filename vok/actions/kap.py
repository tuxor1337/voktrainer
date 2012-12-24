# -*- coding: utf-8 -*-

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
