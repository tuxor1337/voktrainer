
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


from math import floor
from sys import stdout

class cli_progress():
   def __init__(self,win,text):
      self.txt = text
      self.b = 0

   def update(self,a,b,c="\r"):
      self.b = b
      text = self.txt % (a,b)
      width = 20
      marks = floor(width * (float(a)/float(b)))
      loader = '[' + ('=' * int(marks)) + (' ' * int(width - marks)) + ']'
      stdout.write("%s %s%s" % (text,loader,c))
      stdout.flush()

   def destroy(self):
      if self.b != 0:
         self.update(self.b,self.b," Fertig! \n")
