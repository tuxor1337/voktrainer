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
