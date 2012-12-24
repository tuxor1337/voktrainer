# -*- coding: utf-8 -*-

from ..utils import word_list
from ..core.config import CLI_MODE
if CLI_MODE == True:
   from ..cli.progress import cli_progress as progress
   from ..cli.dialogs import dialog_import, dialog_vok_merge_yn,\
               dialog_vok_merge_edit
   from sys import argv
else:
   from ..gui.dialogs import dialog_vok_merge_yn, dialog_vok_merge_edit,\
               dialog_vok_edit, dialog_vok_rem, dialog_import, dialog_export
   from ..gui.progress import gui_progress as progress

def vok_merge(win,kartei,orig,new_meanings):
   ergebnis = dialog_vok_merge_yn(win,orig[1])
   if ergebnis == 1:
      merged = set(orig[2].strip("[]").split("][")).union(new_meanings)
      orig[2] = "[%s]" % ("][".join(merged))
      kartei.edit_vok(orig[0],orig[1],orig[2])
      return orig
   elif ergebnis == -1:
      return None
   else:
      return dialog_vok_merge_edit(win,orig[1])
      
def vok_edit(win,kartei,vok):
   response = dialog_vok_edit(win,*vok[1:3])
   if response != vok[1:3]:
      edited = [vok[0]] + response + [vok[3],vok[4],vok[5]]
      if edited[1] != vok[1] and (len(word_list(edited[1])) > 1\
         or kartei.get_duplicate(edited[1],vok[5],vok[3]) != None):
         kartei.rem_vok(vok[0])
         return vok_add(win,kartei,edited[1],edited[2],edited[5],edited[3])
      else:
         kartei.edit_vok(*edited[0:3])
         return [edited]
   return None
      
def vok_add(win,kartei,wrd1,wrd2,spr,kap):
   lst = word_list(wrd1)
   added,i = [],0
   while i < len(lst):
      gefunden = kartei.get_duplicate(lst[i],spr,kap)
      if gefunden != None:
         vok = vok_merge(win,kartei,gefunden,word_list(wrd2))
         if type(vok) == str:
            lst[i]= vok
            continue
      else:
         vok = [0,lst[i],"[%s]" % ("][".join(word_list(wrd2))),spr,kap]
         vok[0] = kartei.add_vok(vok[1],vok[2],vok[3],vok[4])
      if vok != None:
         added.append(vok)
      i += 1
   return added
   
def vok_rem(win,kartei,vokids):
   if dialog_vok_rem(win,len(vokids)):
      kartei.rem_vok(vokids)
      return True
   return False
   
def vok_move(win,kartei,vokids,kapid):
   anz_ids,moved = len(vokids),[]
   if anz_ids > 30:
      prog_w = progress(win,"Verschiebe... %i von %i Vokabeln")
   for i,vokid in  zip(range(1,anz_ids+1),vokids):
      if i%17 == 0 and anz_ids > 30:
         prog_w.update(i,anz_ids)
      vok = kartei.get_vok(vokid)
      if vok[3] == kapid:
         moved.append(vok)
         continue
      if kartei.get_duplicate(vok[1],vok[5],kapid) != None:
         kartei.rem_vok(vok[0])
         moved.extend(vok_add(win,kartei,vok[1],vok[2],vok[5],kapid))
      else:
         kartei.change_kap(vok[0],kapid)
         vok[3] = kapid
         moved.append(vok)
   if anz_ids > 30:
      prog_w.destroy()
   return moved
   
def vok_copy(win,kartei,vokids,kapid):
   anz_ids,copied = len(vokids),[]
   if anz_ids > 30:
      prog_w = progress(win,"Kopieren... %i von %i Vokabeln")
   for i,vokid in  zip(range(1,anz_ids+1),vokids):
      if i%17 == 0 and anz_ids > 30:
         prog_w.update(i,anz_ids)
      vok = kartei.get_vok(vokid)
      if vok[3] == kapid:
         copied.append(vok)
         continue
      added = vok_add(win,kartei,vok[1],vok[2],vok[5],kapid)
      copied.extend(added)
   if anz_ids > 30:
      prog_w.destroy()
   return copied
   
def vok_import(win,kartei,spr,kap):
   filename = dialog_import(win)
   if filename != None:
      with open(filename,"r") as tmp_file:
         kartei.set_commit_mode(False)
         lines = tmp_file.readlines()
         anz_lines = len(lines)
         for i,line in enumerate(lines):
            if line.find("@") == -1:
               continue
            else:
               vok = line.strip().split("@")
               vok_add(win,kartei,vok[0].strip(),vok[1].strip(),spr,kap)
         kartei.set_commit_mode(True)
         return True
   return False
   
def vok_export(win,kartei,spr,kap,kasten):
      filename,format = dialog_export(win)
      if filename == None:
         return False
      if filename[-4:] != ".txt" and format == "txt":
         filename += ".txt"
      elif filename[-5:] != ".html" and format == "html":
         filename += ".html"
      with open(filename,"w") as tmp_file:
         stapel = kartei.get_stapel(spr,kap,kasten)
         output = []
         if format == "html":
            titel = "%s: %s - %s" % tuple(kartei.get_sprachen(spr)[0][1:4])
            output.extend(["<!DOCTYPE html>","<html><head>","<title>"+titel+"</title>",
               '<meta http-equiv="content-type"	content="text/html; charset=UTF-8" />',
               "</head><body><h1>"+titel+"</h1>","<table>"])
         for i,vok in enumerate(stapel):
            if format == "html":
               output.append("<tr><td>%s</td><td>%s</td></tr>\n" % (vok[1],
                  ", ".join(word_list(vok[2]))))
            else:
               output.append("%s@%s\n" % (vok[1],vok[2]))
         if format == "html":
            output.append("</body></html>")
         tmp_file.writelines(output)
         return True
      return False
   
