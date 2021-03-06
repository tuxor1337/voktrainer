# -*- coding: utf-8 -*-
#
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


import unicodedata
from .core.config import IGNORE_CASE

def extended_lower(str_var):
  return_str = str_var.lower()
  upper_chars = ["Ä","Ö","Ü","É","È","Ô","Æ","Ø"]
  lower_chars = ["ä","ö","ü","é","è","ô","æ","ø"]
  for old,new in zip(upper_chars, lower_chars):
          return_str = return_str.replace(old,new)
  return return_str

def switch_case(var_in):
    if not IGNORE_CASE:
        return var_in
    else:
        if type(var_in) == list:
            return [extended_lower(x) for x in var_in]
        else:
            return extended_lower(var_in)

def remove_accents(input_str):
    return_str = input_str
    if type(input_str) == str:
        nkfd_form = unicodedata.normalize('NFKD', input_str)
        return_str = u"".join([c for c in nkfd_form \
                                     if not unicodedata.combining(c)])
    for old,new in zip(["ὁ ","ἡ ","τὸ ","ῤ","ῥ",
                    "ἁ","ἀ","ά","ὰ","ᾶ","ἄ","ἂ","ἅ","ἃ","ἇ","ἆ",
                    "ή","ὴ","ἠ","ἡ","ἣ","ἥ","ἧ","ῆ","ἦ","ἤ","ἢ",
                    "ὠ","ὡ","ὤ","ὢ","ὥ","ὣ","ὧ","ὦ","ῶ","ώ","ὼ",
                    "ί","ὶ","ἱ","ἰ","ἴ","ἲ","ἳ","ἵ",
                    "ύ","ὺ","ὑ","ὐ","ὓ","ὕ","ὔ","ὒ",
                    "ὁ","ό","ὀ","ὄ","ὂ","ὅ","ὃ","ὸ",
                    "ἐ","ἑ","έ","ὲ","ἓ","ἕ","ἒ","ἔ",
                    "Ἑ"],
                    ["","","","ρ","ρ",
                    "α","α","α","α","α","α","α","α","α","α","α",
                    "η","η","η","η","η","η","η","η","η","η","η",
                    "ω","ω","ω","ω","ω","ω","ω","ω","ω","ω","ω",
                    "ι","ι","ι","ι","ι","ι","ι","ι",
                    "υ","υ","υ","υ","υ","υ","υ","υ",
                    "ο","ο","ο","ο","ο","ο","ο","ο",
                    "ε","ε","ε","ε","ε","ε","ε","ε",
                    "ε"]):
        return_str = return_str.replace(old,new)
    return return_str

def sort_cstm(model,iter1,iter2,nr):
    str1=model.get_value(iter1,nr).lower()
    str2=model.get_value(iter2,nr).lower()
    gewinner = ["ohne kapitel","alle kapitel"]
    if "alle kapitel" in [str1,str2]:
        if str1 == "alle kapitel":
            return -1
        return 1
    elif "ohne kapitel" in [str1,str2]:
        if str1 == "ohne kapitel":
            return -1
        return 1
    if str1 == str2:
        return 0
    elif str1 > str2:
        return 1
    else:
        return -1

def sort_utf8(model,iter1,iter2,nr):
    str1=remove_accents(model.get_value(iter1,nr).lower())
    str2=remove_accents(model.get_value(iter2,nr).lower())
    if str1 == str2:
        return 0
    elif str1 > str2:
        return 1
    else:
        return -1

def word_list(vok_str):
    return vok_str.strip("[]").replace("][","#").split("#")

