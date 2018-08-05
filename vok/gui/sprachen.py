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

from .dialogs import dialog_entry
from ..actions.spr import spr_edit,spr_rem,spr_add
from ..actions.kap import kap_add,kap_edit,kap_rem

class gui_sprachen(Gtk.Window):
    def __init__(self,maingui,geometry,kartei):
        Gtk.Window.__init__(self)

        self.parent_gui = maingui
        self.kartei     = kartei
        self.refreshed  = [False,False]

        width = int(180.0*max(1,geometry[0]))
        height = int(200.0*max(1,geometry[1]))
        self.set_size_request(width,height)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("Sprachverwaltung")
        self.set_modal(True)
        self.set_transient_for(self.parent_gui)

        self.spr_store = self.parent_gui.listen[0]
        cell = Gtk.CellRendererText()
        self.select = Gtk.ComboBox.new_with_model(self.spr_store)
        self.select.pack_start(cell, True)
        self.select.add_attribute(cell, 'text', 0)
        self.select.connect("changed",self.refresh_kap)

        self.kapitel = Gtk.TreeStore(str,int,int)
        self.kapliste = Gtk.TreeView(self.kapitel)
        self.kapliste.connect("button_press_event",self.button_press_cb)
        for i,name in zip(range(2),["Kapitel","#Vokabeln"]):
            zelle  = Gtk.CellRendererText()
            spalte = Gtk.TreeViewColumn(name)
            spalte.pack_start(zelle, True)
            spalte.add_attribute(zelle,"text",i)
            spalte.set_resizable(True)
            spalte.set_expand(True)
            self.kapliste.append_column(spalte)

        top_row = Gtk.HBox()
        top_row.pack_start(self.select, True, True, 0)
        but_lst = [(Gtk.STOCK_EDIT,"edit","Sprache bearbeiten"),
                   (Gtk.STOCK_DELETE,"rem","Sprache entfernen"),
                   (Gtk.STOCK_ADD,"add","Sprache hinzufügen")]
        self.icon_buttons = []
        for icon,action,tooltip in but_lst:
            button = Gtk.Button()
            button.set_image(Gtk.Image.new_from_stock(icon,Gtk.IconSize.BUTTON))
            button.set_relief(Gtk.ReliefStyle.NONE)
            button.set_tooltip_text(tooltip)
            button.connect("released", self.spr_button_cb,action)
            top_row.pack_start(button,False,True,0)
            self.icon_buttons.append(button)

        box_alles = Gtk.VBox()
        box_alles.pack_start(top_row,False,True,5)
        self.scrollwin = Gtk.ScrolledWindow()
        self.scrollwin.add(self.kapliste)
        self.scrollwin.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
        box_alles.pack_start(self.scrollwin, True, True, 0)

        self.add(box_alles)
        self.refresh_view()
        self.connect("destroy", self.destroy_cb)
        self.show_all()

    def destroy_cb(self,widget,data=None):
        if self.refreshed[0] == True:
            self.parent_gui.refresh_kap()

    def refresh_view(self):
        self.select.set_active(self.parent_gui.select[0].get_active())
        if len(self.spr_store) == 1 and self.spr_store[0][1] == 0:
            self.icon_buttons[1].set_sensitive(False)
            self.icon_buttons[0].set_sensitive(False)
        else:
            self.icon_buttons[1].set_sensitive(True)
            self.icon_buttons[0].set_sensitive(True)
        self.refresh_kap()

    def refresh_kap(self,widget=None,data=None):
        if self.select.get_active() != -1:
            self.kapitel.clear()
            spr_id = self.spr_store[self.select.get_active()][1]
            for kap in self.kartei.get_kapitel(spr_id):
                self.kapitel.append(None,
                    [kap[1],self.kartei.count_vok(spr_id,kap[0]),kap[0]])
        return True

    def show_context_menu(self,path,but,time):
        kontext = Gtk.Menu()
        if path == None:
            menu_item = Gtk.MenuItem("Kapitel hinzufügen")
            menu_item.connect("activate", self.menuitem_cb, "add_kap")
            kontext.append(menu_item)
        else:
            menu_item = Gtk.MenuItem("Kapitel löschen")
            menu_item.connect("activate", self.menuitem_cb,"rem_kap")
            kontext.append(menu_item)
            menu_item.show()
            menu_item = Gtk.MenuItem("Umbennenen")
            menu_item.connect("activate", self.menuitem_cb,"edit_kap")
            kontext.append(menu_item)
        kontext.show_all()
        kontext.popup(None, None, None, None, but, time)
        self.kontext = kontext

    def menuitem_cb(self,widget,string):
        if string == "rem_kap":
            if kap_rem(self,self.kartei,self.kapitel[self.gewaehlt][2]):
                    self.kapitel.remove(self.kapitel.get_iter(self.gewaehlt))
                    self.refreshed[0] = True
        elif string == "add_kap":
            kap = kap_add(self, self.kartei,
                                self.spr_store[self.select.get_active()][1])
            if kap != None:
             self.refresh_kap()
             self.refreshed[0] = True
        elif string == "edit_kap":
            kap = kap_edit(self,self.kartei,self.kapitel[self.gewaehlt][::-2])
            if kap != None:
                self.kapitel[self.gewaehlt][0] = kap
                self.refreshed[0] = True

    def button_press_cb(self, widget, event):
        if event.button != 3:
            return False
        time = event.time
        pthinfo = self.kapliste.get_path_at_pos(int(event.x), int(event.y))
        if pthinfo is not None:
            path, col, cellx, celly = pthinfo
            self.gewaehlt = path
            self.kapliste.grab_focus()
            self.kapliste.set_cursor(path, col, 0)
            self.show_context_menu(path, event.button, time)
        else:
            self.show_context_menu(None, event.button, time)
        return True

    def select_spr_id(self,sprid):
        for i,x in enumerate(self.spr_store):
            if x[1] == sprid:
                path = i
        self.select.set_active(path)

    def spr_button_cb(self,button,action):
        if action == "add":
            added = spr_add(self,self.kartei)
            if added != None:
                self.parent_gui.refresh_spr()
                self.refresh_view()
                self.select_spr_id(added)
        elif action == "rem":
            if spr_rem(self, self.kartei,
                             self.spr_store[self.select.get_active()][1]):
                self.parent_gui.refresh_spr()
                self.refresh_view()
        elif action == "edit":
            spr_info = self.kartei.get_sprachen(
                self.spr_store[self.select.get_active()][1])[0]
            if spr_edit(self,self.kartei,spr_info) != None:
                self.parent_gui.refresh_spr()
                self.select_spr_id(spr_info[0])
        return True
