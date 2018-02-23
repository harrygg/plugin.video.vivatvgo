# -*- coding: utf-8 -*-
import uuid
import xbmcplugin
from resources.lib.helper import *

if settings.rebuild_user_data or not settings.guid:
  settings.username = ""
  settings.password = ""
  settings.rebuild_user_data = False
  settings.open()
  settings.guid = uuid.uuid4()

params = get_params()
id = params.get("id")
mediaId = params.get("mediaId")
name = params.get("name")
date = params.get("date")
mode = params.get("mode")

if mode == None:
  show_channels()
elif mode == 'show_channel':
  show_channel(id)
elif mode == 'show_days':
  show_days(id)
elif mode == 'show_recordings':
  show_recordings(id, date)
elif mode == 'show_recording':
  show_recording(id, mediaId, name)
elif mode == 'show_settings':
  show_settings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))