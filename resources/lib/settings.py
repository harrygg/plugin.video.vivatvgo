import xbmc
import xbmcaddon

__id__ = 'plugin.video.vivatvgo'
addon = xbmcaddon.Addon(id=__id__)
profile_dir = xbmc.translatePath( addon.getAddonInfo('profile') )
cwd = xbmc.translatePath( addon.getAddonInfo('path') ).decode('utf-8')

def log(msg, level=xbmc.LOGDEBUG):
  try:
    if settings.debug and level == xbmc.LOGDEBUG:
      level = xbmc.LOGNOTICE
    xbmc.log('%s | %s' % (__id__, str(msg).encode('utf-8')), level)
  except Exception as e:
    try: 
      xbmc.log('%s | Logging failure: %s' % (__id__, e), level)
    except: 
      pass
      
class Settings():

  def __getattr__(self, name):
    temp = addon.getSetting(name)
    if temp.lower() == 'true':
      return True
    elif temp.lower() == 'false':
      return False
    elif temp.isdigit():
      return int(temp)
    else:
      return temp

  def __setattr__(self, name, value):
    addon.setSetting(name, str(value))

settings = Settings() 