import os
import sys
import time
import urllib
import base64
import xbmcgui
from datetime import datetime, timedelta
from resources.lib.helper import *

def show_channels():
  channels = get_channels()
  
  if len(channels) > 0:
    for id, c in channels.iteritems():
      li = xbmcgui.ListItem(label = c["name"], 
                            iconImage = c["logo"], 
                            thumbnailImage = c["logo"])
      url = make_url({"id":id, "action":"show_channel"})
      add_listitem_folder(li, url)
      
  else:
    li = xbmcgui.ListItem('Настройки')
    url = make_url({"action": "show_settings"})
    add_listitem(li, url)

def show_channel(id):
  channel = get_channel(id)
  
  if channel and len(channel["playpaths"]) > 0:
    for i in range(0, len(channel["playpaths"])):
      li_title = "%s | НА ЖИВО %s" % (channel["name"], i+1)
  
    if channel.get("desc"):
      li_title += " | %s" % channel["desc"]
      li = xbmcgui.ListItem(label = li_title, 
                            iconImage = channel.get("logo"), 
                            thumbnailImage = channel.get("logo"))
      li.setInfo(type="Video",
                infoLabels={"Title":li_title})
      li.setProperty("IsPlayable", "True")
      url = channel["playpaths"][i] + pua
      add_listitem(li, url)

    url = make_url({"id":id,"action":"show_days"})
    li = xbmcgui.ListItem("Записи")
    add_listitem_folder(li, url)
  
  else:
    notify_error("Не е намерен активен видео поток за канала или нямате абонамент за този канал!".encode('utf-8'), 2000)

def show_days(id):
  for date in get_dates():
    url = make_url({"id":id, "action":"show_recordings", "date":date})
    li = xbmcgui.ListItem(date)
    add_listitem_folder(li, url)
    
def show_recordings(id, date):
  programs = get_recorded_programs(id, date)
  
  if len(programs) == 0:
    notify_error("Няма намерени записи!")
  
  elif programs[0].get("Error"):
    notify_error(programs[0]["Error"])
  
  else:
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
      li = xbmcgui.ListItem(name)
      url = make_url({"id":id,
                      "action":"show_recording",
                      "mediaId":mediaId,
                      "name":urllib.quote(name.encode("utf-8"))})
      add_listitem_folder(li, url)

def show_recording(id, mediaId, name):
  playpath = get_stream(id, mediaId)
  
  if playpath:
    name = urllib.unquote(name)
    li = xbmcgui.ListItem(name)
    li.setInfo(type="Video", 
              infoLabels={"Title":name, "Plot":name})
    li.setProperty("IsPlayable", 'True')
    url = playpath + pua
    add_listitem(li, url)
    
  else:
    notify_error("Не е намерен URL на видео поток!".encode('utf-8'), 2000)