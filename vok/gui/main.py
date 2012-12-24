# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk
from time import sleep

from ..core.kartei import vokabelKartei
from ..core.config import KASTEN_ANZ, FILTER_ON
from ..actions.abfrager import vok_abfrager
from ..actions.vok import vok_import, vok_export
from ..utils import sort_cstm

from .anzeige import gui_anzeige
from .sprachen import gui_sprachen
from .eingabe import gui_eingabe
from .abfrage import gui_abfrage

class gui_main(Gtk.Window):
   def __init__(self):
      Gtk.Window.__init__(self)

      screen = Gdk.Screen.get_default()
      self.geometry   = (screen.width()/640.0,screen.height()/480.0,\
             int(screen.width()*0.5),int(screen.height()*0.5))
      width,height = int(500.0*max(1,self.geometry[0])),int(400.0*max(1,self.geometry[1]))
      self.set_size_request(width,height)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.set_title("Vokabeltrainer")

      self.ready    = False
      self.kartei   = vokabelKartei()
      self.buttons  = []
      self.selected = [0,0,0]

      top_row = Gtk.HBox()
      self.listen,self.select = [],[]
      for i in range(3):
         self.listen.append(Gtk.TreeStore(str,int))
         self.listen[-1].set_sort_column_id(0,Gtk.SortType.ASCENDING)
         self.listen[-1].set_sort_func(0,sort_cstm,0)
         cell = Gtk.CellRendererText()
         self.select.append(Gtk.ComboBox.new_with_model(self.listen[i]))
         self.select[i].pack_start(cell, True)
         self.select[i].add_attribute(cell, 'text', 0)
         top_row.pack_start(self.select[i],False,False,5)
      self.select[0].connect("changed",self.changed_cb)
      self.select[1].connect("changed",self.changed_cb)
      self.select[2].connect("changed",self.changed_cb)
      self.listen[2].append(None,["Alle Kästen",0])
      for kasten in range(1,KASTEN_ANZ+1):
         self.listen[2].append(None,["Kasten "+str(kasten),kasten])
      self.anz_vok = Gtk.Label(label="0 Einträge")
      top_row.pack_start(self.anz_vok,False,False,5)
      self.abfragefilter = Gtk.CheckButton(label="Abfragefilter")
      if FILTER_ON == 1:
         self.abfragefilter.set_active(True)
      else:
         self.abfragefilter.set_active(False)
      top_row.pack_end(self.abfragefilter,False,False,5)
      self.buttons.append(Gtk.Button("Abfrage starten"))
      top_row.pack_end(self.buttons[-1],False,False,5)
      self.buttons[-1].connect("released",self.button_cb,"abfr")
      self.buttons[-1].connect("key_press_event",self.button_key_cb,"abfr")
      self.buttons.append(Gtk.Button("Vokabeln eintragen"))
      top_row.pack_end(self.buttons[-1],False,False,5)
      self.buttons[-1].connect("released",self.button_cb,"eintr")
      self.buttons[-1].connect("key_press_event",self.button_key_cb,"eintr")

      self.vokliste = gui_anzeige(self.kartei)

      bottom_row = Gtk.HBox()
      self.buttons.append(Gtk.Button("Importieren aus Datei..."))
      bottom_row.pack_start(self.buttons[-1],False,False,5)
      self.buttons[-1].connect("released", self.button_cb,"import")
      self.buttons.append(Gtk.Button("Exportieren in Datei..."))
      bottom_row.pack_start(self.buttons[-1],False,False,5)
      self.buttons[-1].connect("released", self.button_cb,"export")
      button = Gtk.Button("Kapitel und Sprachen verwalten")
      button.connect("released", self.button_cb,"verw")
      bottom_row.pack_end(button,False,False,5)
      button = Gtk.Button("Lernstand zurücksetzen")
      button.connect("released", self.button_cb,"zurueck")
      bottom_row.pack_end(button,False,False,5)
      
      box_alles = Gtk.VBox()
      box_alles.pack_start(top_row,False,True,5)
      self.scrollwin = Gtk.ScrolledWindow()
      self.scrollwin.add(self.vokliste)
      self.scrollwin.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
      box_alles.pack_start(self.scrollwin,True,True,0)
      box_alles.pack_start(bottom_row,False,True,5)
      self.add(box_alles)
      
      accelgroup = Gtk.AccelGroup()
      self.add_accel_group(accelgroup)
      accelgroup.connect(Gdk.keyval_from_name("q"),Gdk.ModifierType.CONTROL_MASK,Gtk.AccelFlags.VISIBLE,self.accel_cb)

      self.connect("destroy", self.destroy_cb)
      self.show_all()
      self.refresh_all()
      
      Gtk.main()
      
   def accel_cb(self,accel_group,acceleratable,keyval,modifier):
      self.destroy()
        
   def destroy_cb(self,widget,data=None):
      self.kartei.close()
      Gtk.main_quit()
      
   def changed_cb(self,widget):
      for i in range(3):
         if self.selected[i] != self.select[i].get_active() \
            and self.select[i].get_active() != -1:
            self.selected[i] = self.select[i].get_active()
            if i == 0:
               self.refresh_kap()
            else:
               self.refresh_vok()
            return True
      
   def refresh_all(self):
      self.refresh_spr()
      self.ready = True
      
   def refresh_spr(self):
      self.listen[0].clear()
      for sprache in self.kartei.get_sprachen():
         self.listen[0].append(None,[sprache[1],sprache[0]])
      if len(self.listen[0]) == 0:
         self.listen[0].append(None,["---",0])
         for button in self.buttons:
            button.set_sensitive(False)
         for sel in self.select:
            sel.set_sensitive(False)
      else:
         for button in self.buttons:
            button.set_sensitive(True)
         for sel in self.select:
            sel.set_sensitive(True)
      self.select[0].set_active(0)
      self.refresh_kap()
      
   def refresh_kap(self):
      if self.select[0].get_active() != -1:
         self.listen[1].clear()
         self.listen[1].append(None,["Alle Kapitel",-1])
         if self.listen[0][0][1] != 0:
            for kapitel in self.kartei.get_kapitel(self.listen[0][self.selected[0]][1]):
                  self.listen[1].append(None,[kapitel[1],kapitel[0]])
         self.listen[1].append(None,["Ohne Kapitel",0])
         self.select[1].set_active(0)
         self.select[2].set_active(0)
         self.refresh_vok()
      return True
      
   def refresh_vok(self):
      if self.select[0].get_active() != -1 and self.select[1].get_active() != -1 \
         and self.select[2].get_active() != -1:
         self.vokliste.show_stapel(self.listen[0][self.selected[0]][1],
            self.listen[1][self.selected[1]][1],
            self.listen[2][self.selected[2]][1])
      self.refresh_anz_vok()
      return True
      
   def refresh_anz_vok(self):
      if self.select[0].get_active() != -1 and self.select[1].get_active() != -1 \
         and self.select[2].get_active() != -1:
         self.anz_vok.show()
         self.buttons[0].set_sensitive(True)
         if len(self.vokliste.vok_store) == 0:
            self.buttons[0].set_sensitive(False)
         if len(self.vokliste.vok_store) == 1:
            self.anz_vok.set_text("1 Eintrag")
         else:
            self.anz_vok.set_text("%d Einträge" % (len(self.vokliste.vok_store)))
      else:
         self.anz_vok.hide()
         
   def button_key_cb(self,widget,event,data):
      if event.type == Gdk.EventType.KEY_PRESS and event.keyval == Gdk.keyval_from_name("Return"):
         self.button_cb(widget,data)
         return True
      
   def button_cb(self,button,data):
      if data == "verw":
         gui_sprachen(self,self.geometry,self.kartei)
      elif data == "eintr":
         gui_eingabe(self,self.geometry,self.kartei,
            self.listen[0][self.selected[0]][1],
            self.listen[1][self.selected[1]][1])
      elif data == "abfr":
         gui_abfrage(self,vok_abfrager(self.kartei,
            self.listen[0][self.selected[0]][1],
            self.listen[1][self.selected[1]][1],
            self.listen[2][self.selected[2]][1],
            self.abfragefilter.get_active()),self.geometry)
      elif data == "zurueck":
         for vok in self.vokliste.vok_store:
            if vok[3] != "Kasten 1":
               self.kartei.change_kasten(vok[4],1)
               self.kartei.touch_vok(vok[4],True)
         self.refresh_vok()
      elif data == "import":
         if vok_import(self,self.kartei,self.listen[0][self.selected[0]][1],\
               self.listen[1][self.selected[1]][1]):
            self.refresh_vok()
      elif data == "export":
         vok_export(self,self.kartei,
               self.listen[0][self.selected[0]][1],
               self.listen[1][self.selected[1]][1],
               self.listen[2][self.selected[2]][1])
      return True
