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


from gi.repository import Gtk, Gdk
from time import sleep
from pkg_resources import resource_filename

from ..core.kartei import vokabelKartei
from ..core.config import KASTEN_ANZ, FILTER_ON
from ..actions.abfrager import vok_abfrager
from ..actions.vok import vok_import, vok_export
from ..utils import sort_cstm

from .anzeige import gui_anzeige
from .sprachen import gui_sprachen
from .eingabe import gui_eingabe
from .abfrage import gui_abfrage

class gui_main(object):
    def __init__(self):
        self.ready    = False

        builder = Gtk.Builder()
        builder.add_from_file(resource_filename("vok.gui", "main.glade"))
        builder.connect_signals(self)

        self.win = builder.get_object("window1")
        screen = Gdk.Screen.get_default()
        self.geometry   = (screen.width()/640.0,screen.height()/480.0,\
                           int(screen.width()*0.5),int(screen.height()*0.5))
        width = int(600.0*max(1,self.geometry[0]))
        height = int(400.0*max(1,self.geometry[1]))
        self.win.set_size_request(width, height)

        self.kartei   = vokabelKartei()
        self.vokliste = gui_anzeige(self, builder.get_object("anzeige"))
        self.anz_vok = builder.get_object("anz_vok")

        self.selected = [0,0,0]
        self.listen, self.select = [], []
        for i in ["sprache","kapitel","kasten"]:
            self.listen.append(builder.get_object("store_%s" % i))
            self.listen[-1].set_sort_column_id(0,Gtk.SortType.ASCENDING)
            self.listen[-1].set_sort_func(0,sort_cstm,0)
            self.select.append(builder.get_object("sel_%s" % i))
        for kasten in range(1,KASTEN_ANZ+1):
            self.listen[2].append(["Kasten "+str(kasten), kasten])

        self.abfragefilter = builder.get_object("abfragefilter")
        if FILTER_ON == 1:
            self.abfragefilter.set_active(True)
        else:
            self.abfragefilter.set_active(False)

        self.buttons  = [
            builder.get_object("button%d" % i) for i in range(1,7)
        ]
        self.buttons[0].connect("released", self.button_cb, "abfr")
        self.buttons[0].connect("key_press_event", self.button_key_cb, "abfr")
        self.buttons[1].connect("released", self.button_cb,"eintr")
        self.buttons[1].connect("key_press_event", self.button_key_cb, "eintr")
        self.buttons[2].connect("released", self.button_cb, "import")
        self.buttons[3].connect("released", self.button_cb, "export")
        self.buttons[4].connect("released", self.button_cb, "verw")
        self.buttons[5].connect("released", self.button_cb, "zurueck")

        builder.get_object("accelgroup") \
               .connect(Gdk.keyval_from_name("q"),
                        Gdk.ModifierType.CONTROL_MASK,
                        Gtk.AccelFlags.VISIBLE,
                        self.accel_cb)

        self.win.show_all()
        self.refresh_all()
        Gtk.main()

    def accel_cb(self, accel_group, acceleratable, keyval, modifier):
        self.win.destroy()

    def destroy_cb(self, widget, data=None):
        self.kartei.close()
        Gtk.main_quit()

    def changed_cb(self, widget):
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
            self.listen[0].append([sprache[1],sprache[0]])
        if len(self.listen[0]) == 0:
            self.listen[0].append(["---",0])
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
            self.listen[1].append(["Alle Kapitel",-1])
            if self.listen[0][0][1] != 0:
                kaps = self.listen[0][self.selected[0]][1]
                kaps = self.kartei.get_kapitel(kaps)
                for kapitel in kaps:
                    self.listen[1].append([kapitel[1], kapitel[0]])
            self.listen[1].append(["Ohne Kapitel", 0])
            self.select[1].set_wrap_width(-(len(self.listen[1])//-15))
            self.select[1].set_active(0)
            self.select[2].set_active(0)
            self.refresh_vok()
        return True

    def refresh_vok(self):
        if self.select[0].get_active() != -1 \
           and self.select[1].get_active() != -1 \
           and self.select[2].get_active() != -1:
            self.vokliste.show_stapel(self.listen[0][self.selected[0]][1],
                self.listen[1][self.selected[1]][1],
                self.listen[2][self.selected[2]][1])
        self.refresh_anz_vok()
        return True

    def refresh_anz_vok(self):
        if self.select[0].get_active() != -1 \
           and self.select[1].get_active() != -1 \
           and self.select[2].get_active() != -1:
            self.anz_vok.show()
            self.buttons[0].set_sensitive(True)
            if len(self.vokliste.vok_store) == 0:
                self.buttons[0].set_sensitive(False)
            if len(self.vokliste.vok_store) == 1:
                self.anz_vok.set_text("1 Eintrag")
            else:
                self.anz_vok.set_text("%d Einträge" \
                                      % (len(self.vokliste.vok_store)))
        else:
            self.anz_vok.hide()

    def button_key_cb(self,widget,event,data):
        if event.type == Gdk.EventType.KEY_PRESS \
           and event.keyval == Gdk.keyval_from_name("Return"):
            self.button_cb(widget,data)
            return True

    def button_cb(self,button,data):
        if data == "verw":
            gui_sprachen(self)
        elif data == "eintr":
            gui_eingabe(self, self.listen[0][self.selected[0]][1],
                              self.listen[1][self.selected[1]][1])
        elif data == "abfr":
            gui_abfrage(self, vok_abfrager(self.kartei,
                        self.listen[0][self.selected[0]][1],
                        self.listen[1][self.selected[1]][1],
                        self.listen[2][self.selected[2]][1],
                        self.abfragefilter.get_active()))
        elif data == "zurueck":
            for vok in self.vokliste.vok_store:
                if vok[3] != "Kasten 1":
                    self.kartei.change_kasten(vok[4],1)
                    self.kartei.touch_vok(vok[4],True)
            self.refresh_vok()
        elif data == "import":
            if vok_import(self.win, self.kartei,
                          self.listen[0][self.selected[0]][1],
                          self.listen[1][self.selected[1]][1]):
                self.refresh_kap()
                self.refresh_vok()
        elif data == "export":
            vok_export(self.win, self.kartei,
                self.listen[0][self.selected[0]][1],
                self.listen[1][self.selected[1]][1],
                self.listen[2][self.selected[2]][1])
        return True

