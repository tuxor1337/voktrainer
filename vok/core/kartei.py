# -*- coding: utf-8 -*-

from multiprocessing import Process,Array
from time import time
import sqlite3

from .config import KASTEN_ANZ,VOK_DIR

class vokabelKartei(Process):
   def __init__(self): 
      self.conn = sqlite3.connect(VOK_DIR+"kartei.sqlite")
      self.conn.text_factory = str
      self.c = self.conn.cursor()
      self.c.execute("""CREATE TABLE IF NOT EXISTS sprachen
         (id INTEGER PRIMARY KEY, name TEXT, spr1 TEXT,
          spr2 TEXT)""")
      self.c.execute("""CREATE TABLE IF NOT EXISTS kapitel
         (id INTEGER PRIMARY KEY,  name TEXT, spr_id INT)""")
      self.c.execute("""CREATE TABLE IF NOT EXISTS vokabeln
         (id INTEGER PRIMARY KEY,  spr1 TEXT, spr2 TEXT,
          kap_id INT, kasten INT, spr_id INT, last_date INT)""")
      self.COMMIT_MODE = True
      self.DEBUG_MODE = False

   def close(self):
      self.c.close()

   def commit(self):
      if self.COMMIT_MODE == True and self.DEBUG_MODE == False:
         self.conn.commit()

   def execute(self,query_str,args=()):
      if self.DEBUG_MODE == True:
         print query_str, args
      self.c.execute(query_str,args)

   def set_commit_mode(self,mode):
      if mode == True and self.COMMIT_MODE == False:
         self.COMMIT_MODE = True
         self.commit()
      elif mode == False and self.COMMIT_MODE == True:
         self.COMMIT_MODE = False

   def get_kapitel(self,sprache,kap_id=-1):
      if kap_id != -1:
         self.execute("SELECT * FROM kapitel WHERE spr_id=? AND id=?",(sprache,kap_id))
      else:
         self.execute("SELECT * FROM kapitel WHERE spr_id=?",(sprache,))
      return self.c.fetchall()

   def get_vok(self,vok_id):
      self.execute("SELECT * FROM vokabeln WHERE id=?",(vok_id,))
      return list(self.c.fetchall()[0])

   def get_sprachen(self,spr_id=None):
      if spr_id != None:
         self.execute("SELECT * FROM sprachen WHERE id=?",(spr_id,))
      else:
         self.execute("SELECT * FROM sprachen ORDER BY name ASC")
      return [list(x) for x in self.c.fetchall()]

   def get_stapel(self,sprache,kapitel=-1,kasten=0):
      if kapitel != -1 and kasten != 0:
         self.execute("""SELECT * FROM vokabeln 
            WHERE spr_id=? AND kap_id=? AND kasten=?""",(sprache,kapitel,kasten))
      elif kapitel != -1:
         self.execute("""SELECT * FROM vokabeln 
            WHERE spr_id=? AND kap_id=?""",(sprache,kapitel))
      elif kasten != 0:
         self.execute("""SELECT * FROM vokabeln 
            WHERE spr_id=? AND kasten=?""",(sprache,kasten))
      else:
         self.execute("SELECT * FROM vokabeln WHERE spr_id=?",(sprache,))
      return self.c.fetchall()

   def rem_vok(self,vokids):
      if list != type(vokids):
         vokids = [vokids]
      for vok in vokids:
         self.execute("""DELETE FROM vokabeln WHERE id=?""",(vok,))
      self.commit()

   def rem_kap(self,kap_id):
      self.execute("""DELETE FROM kapitel WHERE id=?""",(kap_id,))
      self.execute("""DELETE FROM vokabeln WHERE kap_id=?""",(kap_id,))
      self.commit()

   def rem_sprache(self,spr_id):
      self.execute("""DELETE FROM sprachen WHERE id=?""",(spr_id,))
      self.execute("""DELETE FROM vokabeln WHERE spr_id=?""",(spr_id,))
      self.execute("""DELETE FROM kapitel WHERE spr_id=?""",(spr_id,))
      self.commit()

   def add_vok(self,*vok):
      kapitel = vok[3]
      if vok[3] == -1:
         kapitel = 0
      self.execute("""INSERT INTO vokabeln(spr1,spr2,kap_id,kasten,spr_id)
         VALUES (?,?,?,?,?)""",(vok[0],vok[1],kapitel,1,vok[2]))
      self.commit()
      return self.c.lastrowid

   def add_sprache(self,name,spr1,spr2):
      self.execute("""INSERT INTO sprachen(name,spr1,spr2)
         VALUES (?,?,?)""",(name,spr1,spr2))
      self.commit()
      return self.c.lastrowid

   def add_kapitel(self,name,spr_id):
      self.execute("""INSERT INTO kapitel(name,spr_id)
         VALUES (?,?)""",(name,spr_id))
      self.commit()
      return self.c.lastrowid

   def edit_sprache(self,spr_id,name,spr1,spr2):
      self.execute("""UPDATE sprachen SET name=?,spr1=?,spr2=? WHERE id=?""",(name,spr1,spr2,spr_id))
      self.commit()

   def edit_kapitel(self,kap_id,name):
      self.execute("""UPDATE kapitel SET name=? WHERE id=?""",(name,kap_id))
      self.commit()

   def edit_vok(self,vok_id,spr1,spr2):
      self.execute("""UPDATE vokabeln SET spr1=?,spr2=? WHERE id=?""",(spr1,spr2,vok_id))
      self.commit()

   def count_vok(self,sprache,kapitel=0,kasten=0):
      if kapitel != 0 and kasten != 0:
         self.execute("""SELECT COUNT(*) FROM vokabeln 
            WHERE spr_id=? AND kap_id=? AND kasten=?""",(sprache,kapitel,kasten))
      elif kasten != 0:
         self.execute("""SELECT COUNT(*) FROM vokabeln 
            WHERE spr_id=? AND kasten=?""",(sprache,kasten))
      elif kapitel != 0:
         self.execute("""SELECT COUNT(*) FROM vokabeln 
            WHERE spr_id=? AND kap_id=?""",(sprache,kapitel))
      else:
         self.execute("""SELECT COUNT(*) FROM vokabeln WHERE spr_id=?""",(sprache,))
      return self.c.fetchall()[0][0]

   def change_kasten(self,vok_id,kasten):
      if kasten <= KASTEN_ANZ:
         self.execute("""UPDATE vokabeln SET kasten=? WHERE id=?""",(kasten,vok_id))
         self.commit()

   def touch_vok(self,vok_id,null=False):
      timestamp = int(time())
      if null:
         timestamp = 0
      self.execute("""UPDATE vokabeln SET last_date=? WHERE id=?""",(timestamp,vok_id))
      self.commit()

   def change_kap(self,vok_id,kapitel):
      self.execute("""UPDATE vokabeln SET kap_id=? WHERE id=?""",(kapitel,vok_id))
      self.commit()

   def get_duplicate(self,spr1,spr_id,kap_id=-1):
      if kap_id != -1:
         self.execute("SELECT * FROM vokabeln WHERE spr1=? AND spr_id=? AND kap_id=?",(spr1,spr_id,kap_id))
      else:
         self.execute("SELECT * FROM vokabeln WHERE spr1=? AND spr_id=?",(spr1,spr_id))
      ergebnis = self.c.fetchall()
      if len(ergebnis) == 0:
         return None
      else:
         return list(ergebnis[0])

