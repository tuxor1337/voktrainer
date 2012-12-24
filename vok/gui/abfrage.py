# -*- coding: utf-8 -*
from gi.repository import Gtk,Gdk,Pango

class gui_abfrage(Gtk.Window):
   def __init__(self,maingui,abfrager,geometry): 
      Gtk.Window.__init__(self)

      if abfrager.vok_gesamt == 0:
         info = Gtk.MessageDialog(maingui,Gtk.DialogFlags.MODAL,
            Gtk.MessageType.INFO,Gtk.ButtonsType.OK,
            """Keine Vokabeln für die Abfrage verfügbar. Versuchen Sie es
            eventuell erneut mit deaktiviertem Abfragefilter.""")
         info.run(); info.destroy(); self.destroy()
         return None

      self.abfr       = abfrager
      self.parent_gui = maingui
      self.parent_gui.hide()

      width,height = int(240.0*max(1,geometry[0])),int(130.0*max(1,geometry[1]))
      self.set_size_request(width,height)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.set_title("Vokabelabfrage")
      self.set_modal(True)
      self.set_transient_for(self.parent_gui)

      self.last_corr         = Gtk.Label(label=" Richtig:")
      self.last_corr.set_line_wrap(True)
      self.last_corr.set_justify(Gtk.Justification.LEFT)
      self.last_corr.set_alignment(0,0)
      self.last_in       = Gtk.Label(label=" Eingabe:")
      self.last_in.set_justify(Gtk.Justification.LEFT)
      self.last_in.set_alignment(0,0)
      self.last_vok      = Gtk.Label(label=" Letzte Vokabel: ")
      self.last_vok.set_justify(Gtk.Justification.LEFT)
      self.last_vok.set_alignment(0,0)
      self.input_field = Gtk.Entry()
      self.input_field.connect("key_press_event",self.key_press_cb)
      self.input_field.set_events(Gdk.EventMask.KEY_PRESS_MASK)
      self.question        = Gtk.Label()
      self.question.set_markup(self.format_text(0,self.abfr.vokabel[1]))
      self.question.set_line_wrap(True)
      self.question.set_justify(Gtk.Justification.CENTER)
      self.question.set_alignment(0.5,0.5)
      def _resize_func(l,s):
         l.set_size_request(s.width-14, -1)
      self.question.connect("size-allocate",_resize_func)
      self.zaehler        = Gtk.Label()
      self.zaehler.set_text("Abgefragt: 0 von %i Vokabeln" % (self.abfr.vok_gesamt))
      self.zaehler2       = Gtk.Label()
      self.zaehler2.set_text("Richtig: 0 (0%)")
      zaehler_box = Gtk.HBox()
      zaehler_box.pack_start(self.zaehler2,False,False,5)
      zaehler_box.pack_end(self.zaehler,False,False,5)

      alles_box         = Gtk.VBox(False,5)
      alles_box.pack_start(self.question,True,True,0)
      alles_box.pack_start(self.last_vok,False,False,0)
      alles_box.pack_start(self.last_in,False,False,0)
      alles_box.pack_start(self.last_corr,False,False,0)
      alles_box.pack_start(self.input_field,False,True,0)
      alles_box.pack_start(zaehler_box,False,False,3)

      self.add(alles_box)
      self.connect("destroy", self.destroy_cb)
      self.show_all()
      self.last_vok.hide()
      self.last_in.hide()
      self.last_corr.hide()

   def destroy_cb(self,widget,data=None):
      self.parent_gui.refresh_vok()
      self.parent_gui.show()

   def format_text(self,label_type,txt):
      if label_type == 0:
         txt = '<span size="20000" weight="bold">%s</span>' % (txt)
      elif label_type > 0:
         attr = ' weight="bold"'
         attr2 = ' style="italic" size="13000"'
         if label_type == 1:
            rgb = "00DD00"
         elif label_type == 2:
            rgb = "EE0000"
         elif label_type == 3:
            rgb = "FFFF00"
         attr2 += ' background="#%s"' % (rgb)
         txt = '%s<span%s>%s</span>' % (txt[0:11],attr2,txt[10:])
         txt = '<span%s>%s</span>%s' % (attr,txt[0:9],txt[10:])
      return txt

   def key_press_cb(self,widget,event):
      if event.keyval == Gdk.keyval_from_name("Return"):
         if self.abfr.uebrig == []:
            self.destroy()
            return(True)
         else:
            tmp_last_vok = self.abfr.vokabel[1]
            tmp_last = ", ".join(self.abfr.vokabel[2].strip("[]").split("]["))
            wrong = self.abfr.check(widget.get_text())
            self.last_vok.show()
            self.last_in.show()
            self.last_corr.show()
            if wrong == -1:
               out_type,out_text=3,"%s, und? " % (", ".join(self.abfr.antworten))
               self.last_vok.hide()
            elif wrong%2 == 0:
               out_type,out_text=1,"%s " % (tmp_last)
               self.last_corr.hide()
            else:
               out_type,out_text=2,"%s " % (tmp_last)
            if wrong > 1:
               q_type, q_text = -1,"Alle Vokabeln abgefragt!"
            else:
               q_type, q_text = 0,self.abfr.vokabel[1]
            self.last_vok.set_markup(" <span weight=\"bold\">Letzte Vokabel:</span> %s" % (tmp_last_vok))
            def tmp_func(x):
               if x == "":
                  return "(keine)"
               return x
            tmp_in = ", ".join([tmp_func(x) for x in self.abfr.antworten_last])
            self.last_in.set_markup(self.format_text(out_type," Eingabe:  %s " % (tmp_in)))
            self.last_corr.set_markup(" <span weight=\"bold\">Richtig:</span> %s" % (out_text))
            if wrong != -1:
               self.question.set_markup(self.format_text(q_type,q_text))
               self.zaehler.set_text("Abgefragt: %i von %i Vokabeln" % (self.abfr.count(),self.abfr.vok_gesamt))
               self.zaehler2.set_text("Richtig: %i (%i%%)" % (self.abfr.count(True),100*self.abfr.count(True)//self.abfr.count()))
            self.input_field.set_text("")
      return(False)
