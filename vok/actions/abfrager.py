
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
