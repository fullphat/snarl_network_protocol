
import sys
import socket
import threading
import socketserver
import snarlnotify
import snp3

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

                elif sys.platform == 'linux2':
                    snarlnotify.notify_linux(result)

                else:               
                  if 'title' in result:
                    print('>>' + result['title'])

                  if 'text' in result:
                    print('>>' + result['text'])

                  if 'icon' in result:
                    print('>>' + result['icon'])

                response = bytes('SNP/3.0 OK\r\nEND\r\n', 'ascii')

              else:
                response = bytes('SNP/3.0 FAILED\r\nEND\r\n', 'ascii')

              self.request.sendall(response)

        # fires once Quit is True and we fall out of the while loop...
        print('Connection from ' + str(self.client_address) + ' was closed')

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "", 9887

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    print('\nSNP3daemon (multi-platform) 0.3\nCopyright (C) 2015 full phat products')
    print('')
    print('Server started on port ' + str(port) + '; press CTRL+C to exit.\n')

    while True:
      try:
        pass

      except KeyboardInterrupt:
        server.shutdown()
        print("\nServer stopped.\n")
        sys.exit()


