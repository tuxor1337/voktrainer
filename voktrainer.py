#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
   from sys import argv
   if len(argv) < 2:
      import gi
      gi.require_version('Gtk', '3.0')
      from gi.repository import Gtk
      from vok.gui.main import gui_main
      gui_main()
   else:
      import vok.core.config
      vok.core.config.CLI_MODE = True
      from vok.core.kartei import vokabelKartei
      kartei = vokabelKartei()
      if argv[1] == "export" and len(argv) >= 3:
         kapitel = -1
         if len(argv) >= 4:
            kapitel = argv[3]
         for vok in kartei.get_stapel(argv[2],kapitel):
            print "%s@%s" % (vok[1],vok[2])
      elif argv[1] == "import" and len(argv) >= 4:
         kapitel = 0
         if len(argv) >= 5:
            kapitel = argv[4]
         from time import sleep
         from vok.actions.vok import vok_import
         vok_import(None,kartei,argv[3],kapitel)
      elif argv[1] == "sprachen":
         for spr in kartei.get_sprachen():
            print "%s: %s [%s-%s]" % (spr[0],spr[1],spr[2],spr[3])
      elif argv[1] in ["kapitel","kap"] and len(argv) >= 3:
         for kap in kartei.get_kapitel(argv[2]):
            print "%s: %s" % (kap[0],kap[1])
      elif argv[1] == "new" and len(argv) >= 4:
         if argv[2] == "kap" and len(argv) >= 5:
            kartei.add_kapitel(argv[4],argv[3])
         if argv[2] == "spr" and len(argv) >= 5:
            kartei.add_sprache(argv[3],argv[4],argv[5])
         
