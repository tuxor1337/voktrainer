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

class dialog_entry(Gtk.Dialog):
   def __init__(self,titel,parent,flags=Gtk.DialogFlags.MODAL):
      Gtk.Dialog.__init__(self,titel,parent,flags,
               (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT))
      self.ok_button = self.add_button(Gtk.STOCK_OK,Gtk.ResponseType.ACCEPT)
      self.set_default_response(Gtk.ResponseType.ACCEPT)
      self.labels  = []
      self.entries = []

   def key_cb(self,widget,event=None):
      if widget.get_text() == "":
         self.ok_button.set_sensitive(False)
         return True
      elif self.ok_button.get_sensitive() == False:
         self.ok_button.set_sensitive(True)
         return True
      return False

   def add_entry(self,label="",oblig=True):
      box = Gtk.HBox()
      if label != "":
         self.labels.append(Gtk.Label(label=label+":"))
         box.pack_start(self.labels[-1],False,False,3)
      else:
         self.labels.append(None)
      self.entries.append(Gtk.Entry())
      if oblig == True:
         self.entries[-1].connect("changed",self.key_cb)
         self.key_cb(self.entries[-1],None)
      self.entries[-1].set_activates_default(True)
      box.pack_start(self.entries[-1],True,True,0)
      self.vbox.pack_start(box,False,False,0)

def dialog_kap_rem(win):
   frage = Gtk.MessageDialog(win,Gtk.DialogFlags.MODAL,
         Gtk.MessageType.QUESTION,(Gtk.ButtonsType.YES_NO),
         "Bist du sicher, dass du das Kapitel und alle darin gespeicherten Vokabeln löschen willst?")
   ergebnis = frage.run()
   frage.destroy()
   if ergebnis == Gtk.ResponseType.YES:
      return True
   return False

def dialog_kap_edit(win,kap):
   popup = dialog_entry("Kapitel bearbeiten",win)
   popup.add_entry("Name")
   popup.entries[0].set_text(kap)
   popup.show_all()
   ergebnis = popup.run()
   edited = popup.entries[0].get_text()
   popup.destroy()
   if ergebnis == Gtk.ResponseType.ACCEPT:
      return edited
   return kap

def dialog_kap_add(win):
   popup = dialog_entry("Kapitel hinzufügen",win)
   popup.add_entry("Name")
   popup.show_all()
   ergebnis = popup.run()
   kap = popup.entries[0].get_text()
   popup.destroy()
   if ergebnis == Gtk.ResponseType.ACCEPT:
      return kap
   return None

def dialog_spr_add(win):
   popup = dialog_entry("Sprache hinzufügen",win)
   for feld in ["Bezeichnung","Abgefragte Sprache","Antwortsprache"]:
      popup.add_entry(feld)
   popup.show_all()
   ergebnis = popup.run()
   spr = [x.get_text().strip() for x in popup.entries]
   popup.destroy()
   if ergebnis == Gtk.ResponseType.ACCEPT:
      return spr
   return None

def dialog_spr_edit(win,name,spr1,spr2):
   popup = dialog_entry("Sprache bearbeiten",win)
   for x,feld in zip([name,spr1,spr2],["Bezeichnung","Abgefragte Sprache","Antwortsprache"]):
      popup.add_entry(feld)
      popup.entries[-1].set_text(x)
   popup.show_all()
   ergebnis = popup.run()
   edited = [x.get_text().strip() for x in popup.entries]
   popup.destroy()
   if ergebnis == Gtk.ResponseType.ACCEPT:
      return edited
   else:
      return [name,spr1,spr2]

def dialog_spr_rem(win):
   frage = Gtk.MessageDialog(win,Gtk.DialogFlags.MODAL,
      Gtk.MessageType.QUESTION,(Gtk.ButtonsType.YES_NO),
      "Bist du sicher, dass du die Sprache und alle gespeicherten Vokabeln löschen willst?")
   ergebnis = frage.run()
   frage.destroy()
   if ergebnis == Gtk.ResponseType.YES:
      return True
   return False


def dialog_vok_rem(win,anz):
   txt = "Bist du sicher, dass du die "
   if anz == 1:
      txt += "ausgewählte Vokabelkarte"
   else:
      txt += "ausgewählten Vokabelkarten"
   txt += " löschen willst?"
   frage = Gtk.MessageDialog(win,Gtk.DialogFlags.MODAL,Gtk.MessageType.QUESTION,
                                                   (Gtk.ButtonsType.YES_NO),txt)
   success = frage.run()
   frage.destroy()
   if success == Gtk.ResponseType.YES:
      return True
   return False


def dialog_vok_edit(win,wrd1,wrd2):
   popup = dialog_entry("Vokabel bearbeiten",win)
   for x in [wrd1,wrd2]:
      popup.add_entry()
      popup.entries[-1].set_text(x)
   popup.show_all()
   ergebnis = popup.run()
   txt = [x.get_text().strip() for x in popup.entries]
   popup.destroy()
   if ergebnis == Gtk.ResponseType.ACCEPT:
      return txt
   else:
      return [wrd1,wrd2]

def dialog_vok_merge_edit(win,vok):
   frage = Gtk.Dialog(None,win,Gtk.DialogFlags.MODAL,
      (Gtk.STOCK_OK,Gtk.ResponseType.ACCEPT,
      Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
   entry = Gtk.Entry()
   entry.set_text(vok)
   entry.set_activates_default(True)
   entry.show()
   frage.vbox.pack_start(entry,True,True,0)
   ergebnis = frage.run()
   gettxt = entry.get_text()
   frage.destroy()
   if ergebnis == Gtk.ResponseType.ACCEPT:
      return gettxt
   return None


def dialog_vok_merge_yn(win,vok):
   frage = Gtk.MessageDialog(win,Gtk.DialogFlags.MODAL,
         Gtk.MessageType.QUESTION,Gtk.ButtonsType.NONE,
         "Es existiert bereits ein Eintrag für \"%s\". Willst du die neue Vokabel mit diesem Eintrag zusammenführen?"
         % (vok))
   frage.add_button(Gtk.STOCK_YES, Gtk.ResponseType.YES)
   frage.add_button(Gtk.STOCK_NO, Gtk.ResponseType.NO)
   frage.add_button("Überspringen", Gtk.ResponseType.DELETE_EVENT)
   ergebnis = frage.run()
   frage.destroy()
   if ergebnis == Gtk.ResponseType.YES:
      return 1
   elif ergebnis == Gtk.ResponseType.DELETE_EVENT:
      return -1
   return 0

def dialog_import(win):
   chosen = Gtk.FileChooserDialog("Importieren aus Datei...",win,
      Gtk.FileChooserAction.OPEN,
      (Gtk.STOCK_OPEN,Gtk.ResponseType.OK,
      Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
   success = chosen.run()
   filename = chosen.get_filename()
   chosen.destroy()
   if success == Gtk.ResponseType.OK:
      return filename
   return None

def dialog_export(win):
   chosen = Gtk.FileChooserDialog("Exportieren in Datei...",win,
      Gtk.FileChooserAction.SAVE,
      (Gtk.STOCK_SAVE,Gtk.ResponseType.OK,
      Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
   chosen.set_do_overwrite_confirmation(True)
   for fil in [["HTML","*.html","html"],["Plain Text","*.txt","txt"]]:
      filefilter = Gtk.FileFilter()
      filefilter.set_name(fil[0])
      filefilter.add_pattern(fil[1])
      filefilter.internal=fil[2]
      chosen.add_filter(filefilter)
   success = chosen.run()
   filename = chosen.get_filename()
   format = chosen.get_filter().internal
   chosen.destroy()
   if success == Gtk.ResponseType.OK:
      return (filename,format)
   return (None,None)
