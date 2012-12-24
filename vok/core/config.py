from ConfigParser import SafeConfigParser
import os

CLI_MODE    = False
VOK_DIR     = os.path.expanduser("~/.config/voktrainer/")

config = SafeConfigParser({
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
