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
