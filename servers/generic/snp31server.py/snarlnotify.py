
"""
    snarlnotify.py -- multi-platform Snarl notification handler

    Defines two functions: notify_osx and notify_linux which will
    generate notification using the OS X (Mavericks and later)
    built-in functionality or via notify-send respectively.

"""

import subprocess
import sys
import os

try:
    import objc
    from Foundation import *
    import AppKit

except ImportError:
    print("snarlnotify.py: ImportError")

try:
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
    #print("snarlnotify.py: got NSUserNotification")

except NameError:
    print("snarlnotify.py: NameError: ")

"""
    void notify_osx(dict content, int delay, bool sound, dict userInfo)

"""

def notify(content):
    
    if sys.platform == 'darwin':
        notify_osx(content)
        return True

    elif sys.platform == 'linux2' or sys.platform == 'linux':
        notify_linux(content)
        return True

    else:               
        print('platform unsupported: ' + sys.platform)
        return True


def notify_osx(content, delay=0, sound=False, userInfo={}):

    if 'title' in content:
        title = content['title']

    else:
        title = ''

    if 'text' in content:
        text = content['text']

    else:
        text = ''


    if 'source' in content:
        subtext = content['source']

    elif 'x-subtext' in content:
        subtext = content['x-subtext']

    else:
        subtext = ''

    # create the notification object

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(text)
    notification.setInformativeText_(subtext)
    notification.setUserInfo_(userInfo)

    if 'icon' in content:
        icon = content['icon']

        if icon.startswith('!'):
            # translate to stock icon, otherwise assume full path specified
            icon = os.getcwd() + '/icons/' + icon[1:] + '.png'

        appIcon = AppKit.NSImage.alloc().initWithContentsOfFile_("./app.png")
        theIcon = AppKit.NSImage.alloc().initWithContentsOfFile_(icon)

        try:
            notification.setValue_forKey_(theIcon, "_identityImage")
            notification.setValue_forKey_(False, "_identityImageHasBorder")
   
        except:
            print("couldn't set _identityImage")
            notification.setContentImage_(theIcon)

    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")

    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

"""
    void notify_linux(dict content)

"""

def notify_linux(content):

    if 'title' in content:
        title = '"' + content['title'] + '"'

    else:
        title = ''

    if 'text' in content:
        text = '"' + content['text'] + '"'

    else:
        text = ''

    if 'icon' in content:
        icon = content['icon']

        if icon.startswith('!'):
            # translate to stock icon, otherwise assume full path specified
            icon = os.getcwd() + '/icons/' + icon[1:] + '.png'

        else:
            icon = os.getcwd() + '/' + icon

        icon = '-i "' + icon + '" '

    else:
        icon = ''

    print('notify-send ' + icon + title + ' ' + text)

    subprocess.call('notify-send ' + icon + title + ' ' + text, shell=True)

if __name__ == "__main__":

    print("Testing...")
    content = { }
    content["title"] = "Hello world!"
    content["text"] = "Snarl power comes to *IX!"
    notify(content)
    print("A notification should have appeared...")


