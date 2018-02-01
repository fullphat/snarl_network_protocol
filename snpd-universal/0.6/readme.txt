
snd-universal

A simple Snarl Network Protocol (SNP) 3.0 server for cross-platform use
Copyright (C) 2015-2018 full phat products

When launched, opens a TCP socket on the specified port (or 9887 if none provided) and listens for incoming SNP/3.0 packets.

If run on MacOS (Mavericks or later), it will generate notifications using the built-in OS X notification system; if run on Ubuntu (or any other Linux platform which includes "notify-send”), it will generate notifications using that tool.


Command-line:

	python3.4/snpd.py [port=9887]


Revision history:

0.6 - Can now specify $<icon> so operating systems like Elementary OS will use native icons

0.5 - Minor cosmetic enhancements.  Decoded icons are now stored
	  in "./icons/cached/"

0.4 - Added support for custom icons in OS X.  Added support for
	  phat64-encoded icons sent by Snarl.

0.3 - Combined into single multi-platform release.

0.2 - Added icon support to Linux.  Better error checking.

0.1 - First release, different package for OS X and Linux.  Only
	  provided basic functionality.

