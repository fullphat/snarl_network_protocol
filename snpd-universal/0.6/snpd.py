
"""

SNPd -- Snarl Network Protocol daemon for cross-platform use.
Copyright (C) 2015 full phat products

When launched, opens a TCP socket on the specified port (or 9887 if
none provided) and watches for incoming SNP/3.0 packets.  If run on
OS X Mavericks or later, it will generate notifications using the
built in OS X notification system.  If run on Ubuntu or any other
Linux platform which includes "notify-send", it will generate
notifications using that.


Command-line:

	python3.4/snpd.py [port=9887]


Revision history:

0.5 - Minor cosmetic enhancements.  Decoded icons are now stored
	  in "./icons/cached/"

0.4 - Added support for custom icons in OS X.  Added support for
	  phat64-encoded icons sent by Snarl.

0.3 - Combined into single multi-platform release.

0.2 - Added icon support to Linux.  Better error checking.

0.1 - First release, different package for OS X and Linux.  Only
	  provided basic functionality.


"""

import sys
import socket
import threading
import socketserver
import snarlnotify
import snp3
import os

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('Connection from ' + str(self.client_address) + ' opened')
        quit = False
        while not quit:
            data = ''
            while not data.endswith('\r\nEND\r\n'):
              # keep building data until end marker is received
              pkt = str(self.request.recv(1024), 'ascii', 'ignore')
              #print(pkt)

              if pkt == '':
                # recv() returns empty string on error/disconnect
                quit = True
                break

              else:
                # add what was received to data
                data += pkt

            # pretty klunky, but if data was received, process it now
            if not quit:
              result = {}
            
              if snp3.DecodeRequest(data, result):

                if sys.platform == 'darwin':
                    snarlnotify.notify_osx(result)
                    response = bytes('SNP/3.0 OK\r\nEND\r\n', 'ascii')

                elif sys.platform == 'linux2' or sys.platform == 'linux':
                    snarlnotify.notify_linux(result)
                    response = bytes('SNP/3.0 OK\r\nEND\r\n', 'ascii')

                else:               
                    print('platform is ' + sys.platform)

                    if 'title' in result:
                        print('>>' + result['title'])

                    if 'text' in result:
                        print('>>' + result['text'])

                    if 'icon' in result:
                        print('>>' + result['icon'])

                    response = bytes('SNP/3.0 FAILED\r\nEND\r\n', 'ascii')

              else:
                response = bytes('SNP/3.0 FAILED\r\nEND\r\n', 'ascii')

              self.request.sendall(response)

        # fires once Quit is True and we fall out of the while loop...
        print('Connection from ' + str(self.client_address) + ' was closed')

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":

    startport = 9887

    print('\nSNP3daemon (multi-platform) 0.5\nCopyright (C) 2015 full phat products')
    print('')


    if len(sys.argv) > 1:
        try:
            startport = int(sys.argv[1])
        except ValueError:
            print('Invalid TCP port specified.')
            sys.exit(0)

    print('Trying port ' + str(startport) + '...')

    server = ThreadedTCPServer(("", startport), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    if not os.path.exists('icons/cached'):
        os.makedirs('icons/cached')

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    print('SNP 3.0 server started on port ' + str(port) + '; press CTRL+C to exit.\n')

    while True:
      try:
        pass

      except KeyboardInterrupt:
        server.shutdown()
        print("\nServer stopped.\n")
        sys.exit()


