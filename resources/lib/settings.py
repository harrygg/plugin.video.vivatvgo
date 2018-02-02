import os
import xbmc
import xbmcaddon
import cookielib

__id__ = 'plugin.video.vivatvgo'
addon = xbmcaddon.Addon(id=__id__)
profile_dir = xbmc.translatePath( addon.getAddonInfo('profile') )
cookie_file = os.path.join(profile_dir, '.cookies')
channels_file = os.path.join(profile_dir, '.channels')
programs_file = os.path.join(profile_dir, '.programs')
response_file = os.path.join(profile_dir, 'last_response.txt')
cwd = xbmc.translatePath( addon.getAddonInfo('path') ).decode('utf-8')

def log(msg, level=xbmc.LOGDEBUG):
  try:
    if settings.debug and level == xbmc.LOGDEBUG:
      level = xbmc.LOGNOTICE
    xbmc.log('%s | %s' % (__id__, str(msg).encode('utf-8')), level)
  except Exception as e:
    try: 
      xbmc.log('Logging Failure: %s' % (e), level)
    except: 
      pass
      
class Settings():

  def __getattr__(self, name):
    temp = addon.getSetting(name)
    if temp in ['true', 'True']:
      return True
    if temp in ['false', 'False']:
      return False
    if temp.isdigit():
      return int(temp)
    return temp

  def __setattr__(self, name, value):
    addon.setSetting(name, str(value))

settings = Settings() 