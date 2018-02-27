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

def show_channels():
  channels = get_channels()
  if len(channels) > 0:
    for id,c in channels.iteritems():
      li = xbmcgui.ListItem(c["name"], iconImage = c["logo"], thumbnailImage = c["logo"])
      url = make_url({"id":id, "mode":"show_channel"})
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, True) 
  else:
    li = xbmcgui.ListItem('Настройки')
    url = make_url({"mode": "show_settings"})
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

    url = make_url({"id":id, "mode":"show_days"})
    li = xbmcgui.ListItem("Записи")
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, True)
  else:
    notify_error("Не е намерен активен видео поток за канала или нямате абонамент за този канал!".encode('utf-8'), 2000)

def show_days(id):
  for date in get_dates():
    url = make_url({"id":id, "mode":"show_recordings", "date":date})
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
      url = make_url({"id":id,"mode":"show_recording","mediaId":mediaId,"name":urllib.quote(name.encode("utf-8"))})
      log(url)
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, li, True)

def show_recording(id, mediaId, name):
  playpath = get_stream(id, mediaId)
  if playpath:
    name = urllib.unquote(name)
    li = xbmcgui.ListItem(name)
    li.setInfo( type = "Video", infoLabels = { "Title" : name, "Plot": name} )
    li.setProperty("IsPlayable", str(True))
    u = playpath + pua
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False) 
  else:
    notify_error("Не е намерен URL на видео поток!".encode('utf-8'), 2000)

def update(name, location, crash=None):
  lu = settings.last_update
  day = time.strftime("%d")
  if lu != day:
    settings.last_update = day
    p = {}
    p['an'] = get_addon_name()
    p['av'] = get_addon_version()
    p['ec'] = 'Addon actions'
    p['ea'] = name
    p['ev'] = '1'
    p['ul'] = xbmc.getLanguage()
    p['cd'] = location
    import ga
    ga.ga('UA-79422131-12').update(p, crash)

update("Init", "Categories")