
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

class gui_progress(Gtk.Window):
   def __init__(self,win,text):
      Gtk.Window.__init__(self)
      self.text = text
      self.set_decorated(False)
      width,height = 300,80
      self.set_size_request(width,height)
      self.set_skip_taskbar_hint(True)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.set_resizable(False)
      self.set_modal(True)
      self.set_transient_for(win)
      progress = Gtk.ProgressBar()
      status   = Gtk.Label(label="")
      vbox = Gtk.VBox()
      vbox.pack_start(progress,True,True,10)
      vbox.pack_start(status,True,True,5)
      align = Gtk.HBox()
      align.pack_start(vbox,True,True,10)
      frame = Gtk.Frame()
      frame.add(align)
      self.add(frame)
      self.progress = progress
      self.status   = status
      self.show_all()

   def update(self,a,b):
      self.status.set_text(self.text % (a,b))
      self.progress.set_fraction(float(a)/b)
      while Gtk.events_pending():
         Gtk.main_iteration()
