from random import choice
from time import time
from ..utils import switch_case

class vok_abfrager:
   def __init__(self,kartei,sprache,kapitel,kasten,vok_filter=False):
      self.kartei      = kartei
      self.uebrig      = self.kartei.get_stapel(sprache,kapitel,kasten)
      if vok_filter:
         now = int(time())
         delta = 86400
         self.uebrig = [x for x in self.uebrig if int(x[6]) <= now - (x[4]-1)*delta]
      self.vok_gesamt  = len(self.uebrig)
      self.vok_richtig = 0
      if self.vok_gesamt != 0:
             self.vokabel  = choice(self.uebrig)
      self.antworten = []

   def count(self,richtig=False):
      if richtig:
         return self.vok_richtig
      return self.vok_gesamt-len(self.uebrig)

   def check(self,antwort):
      vergleich = set(switch_case(self.vokabel[2].strip("[]").split("][")))
      self.antworten_last = self.antworten
      if switch_case(antwort) in vergleich-set(switch_case(self.antworten)):
         if len(self.antworten)+1 < len(vergleich):
            wrong = -1
         else:
            wrong = 0
            self.vok_richtig += 1
            self.kartei.change_kasten(self.vokabel[0],self.vokabel[4]+1)
      else:
         wrong = 1
         self.kartei.change_kasten(self.vokabel[0],1)
      self.antworten.append(antwort)
      if wrong >= 0:
         self.kartei.touch_vok(self.vokabel[0])
         self.uebrig.remove(self.vokabel)
         if self.uebrig == []:
            wrong += 2
         else:
            self.antworten = []
            self.vokabel   = choice(self.uebrig)
      return wrong
