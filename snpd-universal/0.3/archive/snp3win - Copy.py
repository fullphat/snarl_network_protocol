
import subprocess
#import Foundation
#import objc
#import AppKit
import sys
import os

import base64
import uuid

#NSUserNotification = objc.lookUpClass('NSUserNotification')
#NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

def notify(title, text, subtext, delay=0, sound=False, userInfo={}):
    pass
"""
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(text)
    notification.setInformativeText_(subtext)
    notification.setUserInfo_(userInfo)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
"""

def DecodeRequest(request):

  content = request.splitlines()
  print (content)

  # validate: should start with 'SNP/3.0' and end with 'END'

  if content[0] != 'SNP/3.0':
    print('Invalid request')
    return False

  elif content[len(content)-1] != 'END':
    print('Invalid request')
    return False

  else:
    # process each line

    for line in content[1:len(content)-1]:
      # get the command
      entry = line.split('?')
      command = entry[0]

      if command == 'register' or command == 'unregister' or command == 'addclass':
        print('ignoring command: ' + command)

      elif command == 'notify':
        # notify must have args supplied...
        if len(entry) == 2:
          # translate the args into a dictionary
          args = entry[1].split('&')
          # create an empty dictionary
          d = {}
          for arg in args:
            a = arg.split('=')
            if len(a) == 2:
                #print(a[0] + ' --> ' + a[1])
                # add to the dictionary (quoting the value element)
                d[a[0]] = '"' + a[1] + '"'

          #print('dict')
          #print(d)

          if 'title' in d:
            ttl = d['title']

          else:
            ttl = ''

          if 'text' in d:
            txt = d['text']

          else:
            txt = ''

          # icon

          if 'icon' in d:
            icn = d['icon']

          elif 'icon-phat64' in d:
            icn = d['icon-phat64']              # get the encoded data
            icn = icn.replace('#', '\r\n')      # replace...
            icn = icn.replace('%', '=')         # ...some bits first
            icn = base64.b64decode(icn)         # decode
            uxd = uuid.uuid4()                  # create a UUID

            del d['icon-phat64']
            d['icon'] = str(uxd) + '.png'

            f = open(d['icon'], 'wb')           # save
            f.write(icn)
            f.close()

          else:
            icn = ''

          notify(ttl, txt, "")

        else:
          print('Notify requires arguments')

      else:
        print('Unknown command: ' + command)

    return True

