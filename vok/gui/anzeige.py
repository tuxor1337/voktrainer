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


from gi.repository import Gtk,Gdk

from ..utils import sort_utf8, word_list
from ..actions.vok import vok_edit,vok_rem,vok_add,vok_move,vok_copy
from .progress import gui_progress

class gui_anzeige(object):
    def __init__(self, main, treeview):
        self.main = main
        self.tv = treeview
        self.vok_store = self.tv.get_model()
        self.kartei = main.kartei
        self.tv.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        self.spalten = self.tv.get_columns()
        self.vok_store.set_default_sort_func(lambda x,y,z,w: False)
        self.vok_store.set_sort_func(0, sort_utf8, 0)
        self.vok_store.set_sort_func(1, sort_utf8, 1)

        self.tv.connect("button_press_event", self.button_press_cb)
        self.tv.connect("button_release_event", self.button_release_cb)
        self.tv.connect("key_press_event", self.button_key_cb)

    def show_stapel(self,sprache,kapitel,kasten):
        if sprache == 0:
            return False

        self.info = [sprache,kapitel,kasten]

        self.vok_store.set_sort_column_id(-1,Gtk.SortType.ASCENDING)
        spr_info = self.kartei.get_sprachen(sprache)[0]
        self.spalten[0].set_title(spr_info[2])
        self.spalten[1].set_title(spr_info[3])

        self.vok_store.clear()
        prog_w = gui_progress(self.tv.get_toplevel(),
                              "Auflisten... %i von %i Vokabeln")
        stapel = self.kartei.get_stapel(sprache,kapitel,kasten)
        self.tv.hide()
        for i,vok in zip(range(1,len(stapel)+1),stapel):
            if i%31 == 0:
                prog_w.update(i,len(stapel))
            if vok[3] <= 0:
                kap = "Ohne Kapitel"
            else:
                kap = self.kartei.get_kapitel(sprache,vok[3])[0][1]
            self.vok_store.append([vok[1],
                    ", ".join(vok[2].strip("[]").split("][")),
                    kap,"Kasten "+str(vok[4]),vok[0]])
        prog_w.destroy()
        self.tv.show()
        return True

    def menuitem_cb(self,widget,string,kap=None):
        if string == "del":
            self.menuitem_cb_del(widget, string, kap)
        elif string == "edit":
            self.edit_dialog()
        elif kap != None:
            self.menuitem_cb_move(widget, string, kap)

    def menuitem_cb_del(self, widget, string, kap):
        sel = self.tv.get_selection().get_selected_rows()
        anz_rows = len(sel[1])
        vokids = [self.vok_store[path][4] for path in sel[1]]
        if vok_rem(self.tv.get_toplevel(),self.kartei,vokids):
            if anz_rows > 30:
                self.tv.hide()
                self.main.anz_vok.hide()
            for row in [Gtk.TreeRowReference.new(sel[0],x) for x in sel[1]]:
                self.vok_store.remove(self.vok_store.get_iter(row.get_path()))
            self.main.refresh_anz_vok()
            if anz_rows > 30:
                self.tv.show()
                self.main.anz_vok.show()

    def menuitem_cb_move(self, widget, string, kap):
        sel = self.tv.get_selection().get_selected_rows()
        anz_rows = len(sel[1])
        vokids = [self.vok_store[path][4] for path in sel[1]]
        if string == "copy":
            result = vok_copy(self.tv.get_toplevel(), self.kartei, vokids, kap[1])
            for res in result:
                self.add_vok_to_tree(res[0])
        elif string == "move":
            result = vok_move(self.tv.get_toplevel(), self.kartei, vokids, kap[1])
        if anz_rows > 30:
            self.tv.hide()
            self.main.anz_vok.hide()
        i = -1
        for row in [Gtk.TreeRowReference.new(sel[0],x) for x in sel[1]]:
            vok = self.vok_store[row.get_path()]
            i += 1
            if vok[2] == kap[0]:
                continue
            if i >= len(result) or result[i][1] != vok[0]:
                i -= 1
                continue
            if string != "copy":
                if self.info[1] != -1:
                    treeiter = self.vok_store.get_iter(row.get_path())
                    self.vok_store.remove(treeiter)
                else:
                    if result[i][0] == vok[4]:
                        treeiter = self.vok_store.get_iter(row.get_path())
                        self.vok_store.set(treeiter,2,kap[0])
                    else:
                        self.rem_from_tree(result[i][0])
                        self.edit_tree_vok(row.get_path(),result[i][0])
        self.main.refresh_anz_vok()
        if anz_rows > 30:
            self.tv.show()
            self.main.anz_vok.show()

    def get_path_from_vokid(self, vokid):
        for vok in self.vok_store:
            if vok[4] == vokid:
                return vok.path
                break
        return None

    def rem_from_tree(self, vokid):
        path = self.get_path_form_vokid(vokid)
        if path != None:
            self.vok_store.remove(self.vok_store.get_iter(path))

    def add_vok_to_tree(self, vokid):
        vok = self.kartei.get_vok(vokid)
        if vok[3] <= 0:
            kap = "Ohne Kapitel"
        else:
            kap = self.kartei.get_kapitel(self.info[0],vok[3])[0][1]
        vok2str = ", ".join(word_list(vok[2]))
        newrow = [vok[1], vok2str, kap, "Kasten " + str(vok[4]), vok[0]]
        self.vok_store.append(newrow)

    def edit_tree_vok(self, path, vokid):
        vok = self.kartei.get_vok(vokid)
        if vok[3] <= 0:
            kap = "Ohne Kapitel"
        else:
            kap = self.kartei.get_kapitel(self.info[0],vok[3])[0][1]
        treeiter = self.vok_store.get_iter(path)
        vok2str = ", ".join(word_list(vok[2]))
        self.vok_store.set(treeiter, 0, vok[1],
                                     1, vok2str,
                                     2, kap,
                                     3, "Kasten " + str(vok[4]),
                                     4, vok[0])

    def edit_dialog(self):
        vok = self.kartei.get_vok(self.vok_store[self.gewaehlt][4])
        edited = vok_edit(self.tv.get_toplevel(),self.kartei,vok)
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
        pthinfo = self.tv.get_path_at_pos(int(event.x), int(event.y))
        if event.button == 3:
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                self.gewaehlt = path
                self.tv.grab_focus()
                sel = self.tv.get_selection()
                if sel.count_selected_rows() == 0 \
                    or not sel.path_is_selected(self.gewaehlt):
                    self.tv.set_cursor(path, col, 0)
                kontext = Gtk.Menu()
                if sel.count_selected_rows() == 1:
                    menu_item = Gtk.MenuItem("Bearbeiten")
                    menu_item.connect("activate", self.menuitem_cb, "edit")
                    kontext.append(menu_item)
                menu_item = Gtk.MenuItem("Löschen")
                menu_item.connect("activate", self.menuitem_cb, "del")
                kontext.append(menu_item)
                if len(self.main.listen[1]) > 2:
                    menu_item = Gtk.MenuItem("Verschieben...")
                    menu_item2 = Gtk.MenuItem("Kopieren...")
                    submenu = Gtk.Menu()
                    submenu2 = Gtk.Menu()
                    for kap in list(self.main.listen[1])[1:]:
                        sub_item = Gtk.MenuItem(kap[0])
                        sub_item.connect("activate", self.menuitem_cb,
                                         "move", kap)
                        submenu.append(sub_item)
                        sub_item = Gtk.MenuItem(kap[0])
                        sub_item.connect("activate", self.menuitem_cb,
                                         "copy", kap)
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
        pthinfo = self.tv.get_path_at_pos(int(event.x), int(event.y))
        if event.button == 3:
            return True
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                self.gewaehlt = path
                self.tv.grab_focus()
                self.tv.set_cursor(path, col, 0)
                self.edit_dialog()
            return True

    def button_key_cb(self,widget,event):
        if event.type == Gdk.EventType.KEY_PRESS \
           and event.keyval == Gdk.keyval_from_name("Delete"):
            self.menuitem_cb(widget,"del")
            return True
