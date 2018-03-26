
import sys
import socket
import threading
import socketserver
import snarlnotify
import snp31
import os
import time

ver = "0.3"

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('Connection from ' + str(self.client_address) + ' opened')
        quit = False
        while not quit:
            data = ''
            while not data.endswith('\r\nEND\r\n'):
                # keep building data until end marker is received
                pkt = str(self.request.recv(1024), 'ascii', 'ignore')
                if pkt == '':
                    # recv() returns empty string on error/disconnect
                    quit = True
                    break

                else:
                    # add what was received to data
                    data += pkt

            # pretty klunky, but if data was received, process it now
            if not quit:
                print('[' + data.replace('\r\n', '¬') + ']')

                result = { }
                r,v = snp31.DecodeRequest(data, result)
                if r == 0:
                    snarlnotify.notify(result)
                    response = bytes('SNP/3.1 SUCCESS\r\nEND\r\n', 'ascii')

                else:
                    # failed: r and v contain the number and name respectively
                    response = bytes('SNP/3.1 FAILED\r\nerror-number: ' + str(r) + '\r\nerror-name: ' + v + '\r\nreason: \r\nEND\r\n', 'ascii')

                self.request.sendall(response)

        # fires once Quit is True and we fall out of the while loop...
        print('Connection from ' + str(self.client_address) + ' was closed')

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def do_demo():
    global ver
    content = { }
    content["title"] = "snp31server.py Demo"
    content["text"] = "Gotta love cross-platform goodness..."
    content["source"] = "snp31server v" + ver 
    content["icon"] = os.getcwd() + '/icons/code-python.png'
    snarlnotify.notify(content)


def print_help():
    print('');
    print('Usage: python3.6 snp31server [port]')
    print('[port] will default to 9888 if not supplied')
    print('')
    print('Listens for incoming FORWARD or NOTIFY requests and displays a notification using the local environment where possible.  Currently only macOS and certain Linux platforms are supported.')
    print('Autentication and encryption is not currently supported.')
    print('')


if __name__ == "__main__":

    startport = 9888

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print_help()
            sys.exit(0)

        elif sys.argv[1] == "--demo":
            do_demo()
            sys.exit(0)


    print('\nSNP31server (multi-platform) ' + ver)
    print('Copyright (C) 2017 full phat products')
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

    print('SNP 3.1 server started on port ' + str(port) + '; press CTRL+C to exit.\n')

    while True:
      try:
        time.sleep(0.1)

      except KeyboardInterrupt:
        server.shutdown()
        print("\nServer stopped.\n")
        sys.exit()


