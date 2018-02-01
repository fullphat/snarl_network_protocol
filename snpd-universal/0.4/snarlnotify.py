
"""
    snarlnotify.py -- multi-platform Snarl notification handler

    Defines two functions: notify_osx and notify_linux which will
    generate notification using the OS X (Mavericks and later)
    built-in functionality or via notify-send respectively.

"""

import subprocess
import os

try:
    import Foundation
    import objc
    import AppKit

except ImportError:
    pass

try:
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

except NameError:
    pass

"""
    void notify_osx(dict content, int delay, bool sound, dict userInfo)

"""

def notify_osx(content, delay=0, sound=False, userInfo={}):

    if 'title' in content:
        title = content['title']

    else:
        title = ''

    if 'text' in content:
        text = content['text']

    else:
        text = ''

    if 'subtext' in content:
        subtext = content['subtext']

    else:
        subtext = ''

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

        notification.setContentImage_(AppKit.NSImage.alloc().initWithContentsOfFile_(icon))

	    # broken - claims attribute is read only - credit to Indragie Karunaratne for finding this though...
        #notification.__setattr__('_identityImage', AppKit.NSImage.alloc().initWithContentsOfFile_(icon))
        #setattr(notification, '_identityImage', AppKit.NSImage.alloc().initWithContentsOfFile_(icon))

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

