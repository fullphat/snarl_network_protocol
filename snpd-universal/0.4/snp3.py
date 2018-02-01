
import subprocess
import base64
import uuid
import sys
import os

"""
    bool DecodeRequest(str request, dict result)

    "request" should be a complete SNP 3.0 request, including header and footer.  On successful
    decoding, this function returns True and populates "result" with 'title', 'text' and 'icon'
    if these elements are provided.

    Currently only supports the SNP 3.0 [notify] command.

    Will decode phat64 encoded icons.  Saves them to the working folder as '<UUID>.png' and
    sets result['icon'] to the path.

"""

def DecodeRequest(request, result):

  content = request.splitlines()
  #print (content)

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
                d[a[0]] = a[1]

          #print('dict')
          #print(d)

          if 'title' in d:
            result['title'] = d['title']

          if 'text' in d:
            result['text'] = d['text']

          # icon

          if 'icon' in d:
            result['icon'] = d['icon']

          elif 'icon-phat64' in d:
            icn = d['icon-phat64']              # get the encoded data
            icn = icn.replace('#', '\r\n')      # replace...
            icn = icn.replace('%', '=')         # ...some bits first
            icn = base64.b64decode(icn)         # decode
            uxd = uuid.uuid4()                  # create a UUID

            del d['icon-phat64']
            result['icon'] = 'icons/cached/' + str(uxd) + '.png'

            f = open(result['icon'], 'wb')      # save
            f.write(icn)
            f.close()

        else:
          print('Notify requires arguments')

      else:
        print('Unknown command: ' + command)

    return True

