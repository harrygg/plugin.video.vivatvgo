import os
import sys
import xbmc
import time
import urllib
import base64
import xbmcgui
import xbmcaddon
import xbmcplugin
from datetime import datetime, timedelta
from resources.lib.actions import *

def show_settings():
  addon.openSettings()

def show_channels():
  channels = get_channels()
  if len(channels) > 0:
    for id,c in channels.iteritems():
      li = xbmcgui.ListItem(c["name"], iconImage = c["logo"], thumbnailImage = c["logo"])
      url = "%s?id=%s&mode=show_channel" % (sys.argv[0], id)
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, True) 
  else:
    li = xbmcgui.ListItem('Настройки')
    url = "%s?mode=show_settings" % sys.argv[0]
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li)  

def show_channel(id):
  channel = get_channel(id)
  if channel and len(channel["playpaths"]) > 0:
    for i in range(0, len(channel["playpaths"])):
      li_title = "%s | НА ЖИВО %s" % (channel["name"], i+1)
      if channel.get("desc"):
        li_title += " | %s" % channel["desc"]
      li = xbmcgui.ListItem(li_title, iconImage = channel.get("logo"), thumbnailImage = channel.get("logo"))
      li.setInfo( type = "Video", infoLabels = { "Title" : li_title } )
      li.setProperty("IsPlayable", "True")
      url = channel["playpaths"][i] + pua
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li) 

    url = "%s?id=%s&mode=show_days" % (sys.argv[0], id)
    li = xbmcgui.ListItem("Записи")
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, True)
  else:
    command = "Notification(%s,%s,%s)" % ("Грешка", "Не е намерен активен видео поток за канала или нямате абонамент за този канал!".encode('utf-8'), 2000)
    xbmc.executebuiltin(command) 

def show_days(id):
  for date in get_dates():
    url = "%s?id=%s&mode=show_recordings&date=%s" % (sys.argv[0], id, date)
    li = xbmcgui.ListItem(date)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, True)  
    
def show_recordings(id, date):
  programs = get_recorded_programs(id, date)
  if programs:
    log("Found %s programs" % len(programs))
    for program in programs:
      name = program["name"]
      if program.get("introduce"):
        name += ", " + program["introduce"]
      
      if program.get("starttime"):
        try: 
          dt = datetime.strptime(program["starttime"], '%Y%m%d%H%M00')
        except TypeError:
          dt = datetime.fromtimestamp(time.mktime(time.strptime(program["starttime"], '%Y%m%d%H%M00')))
        
        airtime = dt.strftime('%Y-%m-%d %H:%M ')
        name = airtime + name
      
      id = program["id"]
      try: mediaId = program["recordedMediaIds"][0]
      except: mediaId = 0
      
      logo = ""
      li = xbmcgui.ListItem(name, iconImage = logo, thumbnailImage = logo)
      url = "%s?id=%s&mode=show_recording&mediaId=%s&name=%s" % (sys.argv[0], id, mediaId, urllib.quote(name.encode("utf-8")))
      log(url)
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, True)

def show_recording(id, mediaId, name):
  playpath = get_stream(id, mediaId)
  if playpath:
    name = urllib.unquote(name)
    li = xbmcgui.ListItem(name)
    li.setInfo( type = "Video", infoLabels = { "Title" : name} )
    li.setProperty("IsPlayable", str(True))
    u = playpath + pua
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False) 
  else:
    command = "Notification(%s,%s,%s)" % ("Грешка", "Не е намерен URL на видео поток!".encode('utf-8'), 2000)
    xbmc.executebuiltin(command) 
  
def get_params():
  param = {}
  paramstring = sys.argv[2]
  if len(paramstring) >= 2:
    params = sys.argv[2]
    cleanedparams = params.replace('?','')
    if (params[len(params)-1] == '/'):
      params = params[0:len(params) - 2]
    pairsofparams = cleanedparams.split('&')
    for i in range(len(pairsofparams)):
      splitparams = {}
      splitparams = pairsofparams[i].split('=')
      if (len(splitparams)) == 2:
        param[splitparams[0]] = splitparams[1]
  return param

def update(name, location, crash=None):
  lu = settings.last_update
  day = time.strftime("%d")
  if lu != day:
    settings.last_update = day
    p = {}
    p['an'] = addon.getAddonInfo('name')
    p['av'] = addon.getAddonInfo('version')
    p['ec'] = 'Addon actions'
    p['ea'] = name
    p['ev'] = '1'
    p['ul'] = xbmc.getLanguage()
    p['cd'] = location
    from ga import ga
    ga('UA-79422131-12').update(p, crash)

pua = base64.b64decode("fFVzZXItQWdlbnQ9RXhvUGxheWVyRGVtby8yLjAuMTMgKExpbnV4LEFuZHJvaWQgNy4wKSBFeG9QbGF5ZXJMaWIvMS41Ljg=")
update("Init", "Categories")