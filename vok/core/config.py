
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


from configparser import ConfigParser
import os

CLI_MODE    = False
VOK_DIR     = os.path.expanduser("~/.config/voktrainer/")

config = ConfigParser(defaults={
        'anz_kaesten':'5',
        'ignore_case':'1',
        'abfragefilter':'1'
    })

if not os.path.isdir(VOK_DIR):
    os.makedirs(VOK_DIR)
if not os.path.isfile(VOK_DIR+"config"):
    with open(VOK_DIR+"config",'w') as configfile:
        config.write(configfile)
else:
    config.read(VOK_DIR+"config")

KASTEN_ANZ	= int(config.get("DEFAULT","anz_kaesten"))
IGNORE_CASE	= int(config.get("DEFAULT","ignore_case"))
FILTER_ON	= int(config.get("DEFAULT","abfragefilter"))
