# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk

from ..utils import sort_utf8, word_list
from ..actions.vok import vok_edit,vok_rem,vok_add,vok_move,vok_copy
from .progress import gui_progress

class gui_anzeige(Gtk.TreeView):
   def __init__(self,kartei):
      self.vok_store = Gtk.TreeStore(str,str,str,str,int)
      Gtk.TreeView.__init__(self,self.vok_store)
      self.kartei = kartei
      self.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
      
      self.spalten = []
      for i,name in enumerate(["Abgrefragte Sprache","Antwortsprache",\
                                       "Kapitel","Kasten"]):
             zelle  = Gtk.CellRendererText()
             spalte = Gtk.TreeViewColumn(name)
             spalte.pack_start(zelle,True)
             spalte.add_attribute(zelle,"text",i)
             spalte.set_resizable(True)
             if i <= 1:
               spalte.set_min_width(250)
               spalte.set_max_width(400)
             self.append_column(spalte)
             spalte.set_sort_column_id(i)
             self.spalten.append(spalte)
      self.set_search_column(0)
      self.vok_store.set_default_sort_func(lambda x,y,z,w: False)
      self.vok_store.set_sort_func(0,sort_utf8,0)
      self.vok_store.set_sort_func(1,sort_utf8,1)

      self.connect("button_press_event",self.button_press_cb)
      self.connect("button_release_event",self.button_release_cb)
      self.connect("key_press_event",self.button_key_cb)

   def show_stapel(self,sprache,kapitel,kasten):
      if sprache == 0:
         return False
         
      self.info = [sprache,kapitel,kasten]
      
      self.vok_store.set_sort_column_id(-1,Gtk.SortType.ASCENDING)
      spr_info = self.kartei.get_sprachen(sprache)[0]
      self.spalten[0].set_title(spr_info[2])
      self.spalten[1].set_title(spr_info[3])

      self.vok_store.clear()
      prog_w = gui_progress(self.get_toplevel(),"Auflisten... %i von %i Vokabeln")
      stapel = self.kartei.get_stapel(sprache,kapitel,kasten)
      self.hide()
      for i,vok in zip(range(1,len(stapel)+1),stapel):
         if i%31 == 0:
            prog_w.update(i,len(stapel))
         if vok[3] <= 0:
            kap = "Ohne Kapitel"
         else:
            kap = self.kartei.get_kapitel(sprache,vok[3])[0][1]
         self.vok_store.append(None, [vok[1], 
               ", ".join(vok[2].strip("[]").split("][")),
               kap,"Kasten "+str(vok[4]),vok[0]])
      prog_w.destroy()
      self.show()
      return True

   def menuitem_cb(self,widget,string,kap=None):
      if string == "del":
         selected = self.get_selection().get_selected_rows()
         anz_rows = len(selected[1])
         vokids = [self.vok_store[path][4] for path in selected[1]]
         if vok_rem(self.get_toplevel(),self.kartei,vokids):
            if anz_rows > 30:
               self.hide()
               self.get_toplevel().anz_vok.hide()
            for i,row in  zip(range(1,anz_rows+1),[Gtk.TreeRowReference.new(selected[0],x) for x in selected[1]]):
               self.vok_store.remove(self.vok_store.get_iter(row.get_path()))
            self.get_toplevel().refresh_anz_vok()
            if anz_rows > 30:
               self.show()
               self.get_toplevel().anz_vok.show()
      elif string == "edit":
         self.edit_dialog()
      elif kap != None:
         selected = self.get_selection().get_selected_rows()
         anz_rows = len(selected[1])
         vokids = [self.vok_store[path][4] for path in selected[1]]
         if string == "copy":
            result = vok_copy(self.get_toplevel(),self.kartei,vokids,kap[1])
         elif string == "move":
            result = vok_move(self.get_toplevel(),self.kartei,vokids,kap[1])
         if anz_rows > 30:
            self.hide()
            self.get_toplevel().anz_vok.hide()
         i = -1
         for row in  [Gtk.TreeRowReference.new(selected[0],x) for x in selected[1]]:
            vok = self.vok_store[row.get_path()]
            i += 1
            if vok[2] == kap[0]:
               continue
            if i >= len(result) or result[i][1] != vok[0]:
               i -= 1
               continue
            if string == "copy":
               if self.info[1] == -1:
                  self.edit_tree_vok(self.get_path_from_vokid(result[i][0]),result[i][0])
            else:
               if self.info[1] != -1:
                  self.vok_store.remove(self.vok_store.get_iter(row.get_path()))
               else:
                  if result[i][0] == vok[4]:
                     self.vok_store.set(self.vok_store.get_iter(row.get_path()),2,kap[0])
                  else:
                     self.rem_from_tree(result[i][0])
                     self.edit_tree_vok(row.get_path(),result[i][0])
         self.get_toplevel().refresh_anz_vok()
         if anz_rows > 30:
            self.show()
            self.get_toplevel().anz_vok.show()
            
   def get_path_from_vokid(self,vokid):
      for vok in self.vok_store:
         if vok[4] == vokid:
            return vok.path
            break
      return None
            
   def rem_from_tree(self,vokid):
      path = self.get_path_form_vokid(vokid)
      if path != None:
         self.vok_store.remove(self.vok_store.get_iter(path))
     
   def add_vok_to_tree(self,vokid):
      vok = self.kartei.get_vok(vokid)
      if vok[3] <= 0:
         kap = "Ohne Kapitel"
      else:
         kap = self.kartei.get_kapitel(self.info[0],vok[3])[0][1]
      self.vok_store.append(None,[vok[1],", ".join(word_list(vok[2])),kap,"Kasten "+str(vok[4]),vok[0]])
      
   def edit_tree_vok(self,path,vokid):
      vok = self.kartei.get_vok(vokid)
      if vok[3] <= 0:
         kap = "Ohne Kapitel"
      else:
         kap = self.kartei.get_kapitel(self.info[0],vok[3])[0][1]
      self.vok_store.set(self.vok_store.get_iter(path),0,vok[1],
         1,", ".join(word_list(vok[2])),2,kap,3,"Kasten "+str(vok[4]),4,vok[0])
      
   def edit_dialog(self):
      vok = self.kartei.get_vok(self.vok_store[self.gewaehlt][4])
      edited = vok_edit(self.get_toplevel(),self.kartei,vok)
      if edited != None:
         if len(edited) > 1:
            self.vok_store.remove(self.vok_store.get_iter(self.gewaehlt))
            for eintr in edited:
               self.rem_from_tree(eintr[0])
               self.add_vok_to_tree(eintr[0])
         else:
            row = Gtk.TreeRowReference.new(self.vok_store,self.gewaehlt)
            if vok[0] != edited[0][0]:
               self.rem_from_tree(edited[0][0])
            self.edit_tree_vok(row.get_path(),edited[0][0])
        
   def button_release_cb(self,widget,event):
      pthinfo = self.get_path_at_pos(int(event.x), int(event.y))
      if event.button == 3:
         if pthinfo is not None:
            path, col, cellx, celly = pthinfo
            self.gewaehlt = path
            self.grab_focus()
            sel = self.get_selection()
            if sel.count_selected_rows() == 0 \
               or not sel.path_is_selected(self.gewaehlt):
               self.set_cursor(path, col, 0)
            kontext = Gtk.Menu()
            if sel.count_selected_rows() == 1:
               menu_item = Gtk.MenuItem("Bearbeiten")
               menu_item.connect("activate", self.menuitem_cb, "edit")
               kontext.append(menu_item)
            menu_item = Gtk.MenuItem("Löschen")
            menu_item.connect("activate", self.menuitem_cb, "del")
            kontext.append(menu_item)
            if len(self.get_toplevel().listen[1]) > 2:
               menu_item = Gtk.MenuItem("Verschieben...")
               menu_item2 = Gtk.MenuItem("Kopieren...")
               submenu = Gtk.Menu()
               submenu2 = Gtk.Menu()
               for kap in list(self.get_toplevel().listen[1])[1:]:
                  sub_item = Gtk.MenuItem(kap[0])
                  sub_item.connect("activate", self.menuitem_cb,"move",kap)
                  submenu.append(sub_item)
                  sub_item = Gtk.MenuItem(kap[0])
                  sub_item.connect("activate", self.menuitem_cb,"copy",kap)
                  submenu2.append(sub_item)
               menu_item.set_submenu(submenu)
               menu_item2.set_submenu(submenu2)
               kontext.append(menu_item)
               kontext.append(menu_item2)
            self.kontext = kontext
            self.kontext.show_all()
            self.kontext.popup(None, None, None, None, 0, event.time)
         return True
         
   def button_press_cb(self,widget,event):
      pthinfo = self.get_path_at_pos(int(event.x), int(event.y))
      if event.button == 3:
         return True
      if event.type == Gdk.EventType._2BUTTON_PRESS:
         if pthinfo is not None:
            path, col, cellx, celly = pthinfo
            self.gewaehlt = path
            self.grab_focus()
            self.set_cursor(path, col, 0)
            self.edit_dialog()
         return True
         
   def button_key_cb(self,widget,event):
      if event.type == Gdk.EventType.KEY_PRESS and event.keyval == Gdk.keyval_from_name("Delete"):
         self.menuitem_cb(widget,"del")
         return True
