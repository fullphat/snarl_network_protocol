
## snp31server.py
A Python SNP 3.1 server for macOS and certain* versions of Linux.

Copyright (c) 2017-2018 full phat products

Version 0.3

> *The Linux distribution must support the `notify-send` package and meet the dependencies below

### Dependencies
* Python 3 (tested and working on Python 3.6)
* pyobjc (macOS only)

To install pyobjc:

    python3.6 -m pip install -U pyobjc-core
    python3.6 -m pip install -U pyobjc

### Issues with using https:// icons?

If you're running on Python 3.6 and macOS, be aware that Python 3.6 has no SSL certificates for macOS installed by default.  This will cause any urls that use `https://` to fail.  This can be remedied by running:

`/Applications/Python\ 3.6/Install\ Certificates.command`

### Installing notify-send on Linux

Not all Linux distributions ship with notify-send installed, this can be done with:

    sudo apt install libnotify-bin


### Notes
* Only `NOTIFY` and `FORWARD` are currently supported; other commands are ignored
* This server does not implement the SNPD discovery service

### Change History

#### 0.3
* Defaults to port 9888 rather than 9887
* Now properly only supports NOTIFY and FORWARD (returns NotImplemented for other commands)

#### 0.2
* Better icon handling support
* On macOS, displays icon on the left of the notification

#### 0.1
* Initial test release


