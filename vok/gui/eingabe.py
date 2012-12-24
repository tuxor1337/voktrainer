# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk

from .dialogs import dialog_entry
from ..actions.vok import vok_add,vok_edit,vok_rem

class gui_eingabe(Gtk.Window):
   def __init__(self,maingui,geometry,kartei,sprache,kapitel):
      Gtk.Window.__init__(self)
        
      self.parent_gui = maingui
      self.kartei     = kartei
      if kapitel == -1:
         self.kapitel = 0
      else:
         self.kapitel = kapitel
      self.spr_info   = self.kartei.get_sprachen(sprache)[0]

      width,height = int(190.0*max(1,geometry[0])),int(90.0*max(1,geometry[1]))
      self.set_size_request(width,-1)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.set_title("Vokabeln hinzufügen")
      self.set_modal(True)
      self.set_transient_for(self.parent_gui)
      self.set_skip_taskbar_hint(True)

      box_alles = Gtk.VBox()
      self.input_field = []
      for i,sprache in zip(range(2),[self.spr_info[2],self.spr_info[3]]):
             self.input_field.append(Gtk.Entry())
             self.input_field[i].connect("key_press_event",self.button_cb)
             self.input_field[i].set_events(Gdk.EventMask.KEY_PRESS_MASK)
             hbox        = Gtk.HBox()
             hbox.pack_start(Gtk.Label(sprache),False,False,5)
             hbox.pack_start(self.input_field[i],True,True,5)
             box_alles.pack_start(hbox,False,False,1)
      hbox        = Gtk.HBox()
      button = Gtk.Button("Fertig")
      button.connect("released", lambda x: self.destroy())
      hbox.pack_end(button,False,False,5)
      button = Gtk.Button("Hinzufügen")
      button.connect("released", self.add_vokabel)
      button.connect("key_press_event", self.add_vokabel)
      hbox.pack_end(button,False,False,0)
      box_alles.pack_start(hbox,False,False,1)
      
      self.zuletzt_store = Gtk.TreeStore(str,str,int)
      tree,spalten = Gtk.TreeView(self.zuletzt_store),[]
      for i,name in zip(range(2),["Abgrefragte Sprache","Antwortsprache"]):
         zelle  = Gtk.CellRendererText()
         spalte = Gtk.TreeViewColumn(name)
         spalte.pack_start(zelle, True)
         spalte.add_attribute(zelle,"text",i)
         spalte.set_resizable(True)
         spalte.set_min_width(150)
         spalte.set_max_width(250)
         tree.append_column(spalte)
         spalten.append(spalte)
      tree.connect("button_press_event",self.button_tree_cb)
      tree.connect("key_press_event",self.key_tree_cb)
      spalten[0].set_title(self.spr_info[2])
      spalten[1].set_title(self.spr_info[3])
      scrollwin = Gtk.ScrolledWindow()
      scrollwin.add(tree)
      scrollwin.set_size_request(-1,150)
      scrollwin.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)
      box_alles.pack_start(scrollwin,True,True,0)

      self.add(box_alles)
      self.connect("destroy", self.destroy_cb)
      self.show_all()
      self.scrollwin = scrollwin
      self.tree = tree
        
   def destroy_cb(self,widget,data=None):
      if len(self.zuletzt_store) != 0:
         self.parent_gui.refresh_vok()
      
   def add_vokabel(self,widget=None,data=None):
      tmp_eintr = self.input_field[1].get_text()
      tmp_eintr2 = self.input_field[0].get_text()
      
      if tmp_eintr2 == "" and tmp_eintr == "":
            self.destroy()
      if tmp_eintr2 == "" or tmp_eintr == "":
            if tmp_eintr2 != "":
               self.input_field[1].grab_focus()
            return True
      zuletzt = "%s = %s" % (", ".join(tmp_eintr2),", ".join(tmp_eintr.split("#")))
      for eintr in vok_add(self,self.kartei,tmp_eintr2,tmp_eintr,self.spr_info[0],self.kapitel):
         self.rem_from_tree(eintr[0])
         self.add_vok_to_tree(eintr[1],eintr[2],eintr[0])
      self.input_field[0].set_text("")
      self.input_field[1].set_text("")
      self.input_field[0].grab_focus()
   
   def edit_dialog(self):
      vok = self.kartei.get_vok(self.zuletzt_store[self.tree.gewaehlt][2])
      edited = vok_edit(self,self.kartei,vok)
      if edited != None:
         if len(edited) > 1 or edited[0][0] != vok[0]:
            self.zuletzt_store.remove(self.zuletzt_store.get_iter(self.tree.gewaehlt))
            for eintr in edited:
               self.rem_from_tree(eintr[0])
               self.add_vok_to_tree(eintr[1],eintr[2],eintr[0])
         else :
            self.zuletzt_store.set(self.zuletzt_store.get_iter(self.tree.gewaehlt),
                  0, edited[0][1], 1, edited[0][2], 2, edited[0][0])
      
   def rem_from_tree(self,vokid):
      for vok in self.zuletzt_store:
         if vok[2] == vokid:
            self.zuletzt_store.remove(vok.iter)
            break
     
   def add_vok_to_tree(self,spr1,spr2,vokid):
      self.zuletzt_store.insert(None,0,[spr1,spr2,vokid])
      self.tree.get_selection().select_path((0,))
      scrollbar = self.scrollwin.get_vadjustment()
      if scrollbar != None:
         while Gtk.events_pending():
            Gtk.main_iteration()
         scrollbar.set_value(0.0)
      
   def button_tree_cb(self,widget,event=None):
      time = event.time
      pthinfo = self.tree.get_path_at_pos(int(event.x), int(event.y))
      if event.button == 3:
         if pthinfo is not None:
            path, col, cellx, celly = pthinfo
            self.tree.gewaehlt = path
            self.tree.grab_focus()
            self.tree.set_cursor(path, col, 0)
            kontext = Gtk.Menu()
            menu_item = Gtk.MenuItem("Bearbeiten")
            menu_item.connect("activate", self.menuitem_cb, "edit")
            kontext.append(menu_item)
            menu_item = Gtk.MenuItem("Löschen")
            menu_item.connect("activate", self.menuitem_cb, "del")
            kontext.append(menu_item)
            kontext.show_all()
            kontext.popup(None, None, None, None, event.button, time)
            self.kontext = kontext
         return True
      if event.type == Gdk.EventType._2BUTTON_PRESS:
         if pthinfo is not None:
            path, col, cellx, celly = pthinfo
            self.tree.gewaehlt = path
            self.tree.grab_focus()
            self.tree.set_cursor(path, col, 0)
            self.edit_dialog()
         return True
         
   def key_tree_cb(self,widget,event=None):
      if event.type == Gdk.EventType.KEY_PRESS and event.keyval == Gdk.keyval_from_name("Return"):
         sel = self.tree.get_selection()
         if sel.count_selected_rows() > 0:
            self.tree.gewaehlt = sel.get_selected_rows()[1][0]
            self.edit_dialog()
            return True
      return False
         
   def menuitem_cb(self,widget,string):
      if string == "del":
         if vok_rem(self,self.kartei,self.zuletzt_store[self.tree.gewaehlt][2:3]):
            self.zuletzt_store.remove(self.zuletzt_store.get_iter(self.tree.gewaehlt))
      elif string == "edit":
         self.edit_dialog()
   
   def button_cb(self,widget,event=None):
      if (event.type == Gdk.EventType.KEY_PRESS and event.keyval == Gdk.keyval_from_name("Escape")):
         self.destroy()
         return True
      elif (event.type == Gdk.EventType.KEY_PRESS and event.keyval == Gdk.keyval_from_name("Return")) or \
         (event.type == Gdk.EventType.BUTTON_PRESS): 
         self.add_vokabel()
         return True
      elif event.type == Gdk.EventType.KEY_PRESS and event.keyval == Gdk.keyval_from_name("e")\
         and event.state & Gdk.ModifierType.CONTROL_MASK:
         sel = self.tree.get_selection()
         if sel.count_selected_rows() > 0:
            self.tree.gewaehlt = sel.get_selected_rows()[1][0]
            self.edit_dialog()
            return True
      return False
