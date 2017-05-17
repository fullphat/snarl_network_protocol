
import urllib.request
import subprocess
import base64
import uuid
import sys
import os

"""
    bool DecodeRequest(str request, dict result)

    "request" should be a complete SNP 3.1 request, including header and footer.  On successful
    decoding, this function returns True and populates "result" with 'title', 'text' and 'icon'
    if these elements are provided.

    Currently only supports the SNP 3.1 NOTIFY command.

    Will decode phat64 encoded icons.  Saves them to the working folder as '<UUID>.png' and
    sets result['icon'] to the path.

"""

def decode_icon(icon):

  if icon == "":
    return ""

  # should be "<type>:<data>"...
  x = icon.split(':', 1)

  # validate...
  if len(x) != 2:
    return ""

  x[0] = x[0].strip()
  x[1] = x[1].strip()
  if (x[0] == "" or x[1] == ""):
    return ""
 
  # decode based on <type>...

  if x[0] == 'stock':
    return os.getcwd() + '/icons/' + x[1] + '.png'

  elif x[0] == 'file':
    # assume local
    return x[1]

  elif x[0] == 'url':
    # download and save to cache...
    uxd = uuid.uuid4()                  # create a UUID
    path = 'cached/' + str(uxd) + '.png'

    try:
      urllib.request.urlretrieve(x[1], path)
      return path

    except Exception as downloadError:
      print("Couldn't download: " + x[1])
      print(downloadError)
      return ""

  elif x[0] == 'phat64':
    # decode and save to cache...
    icn = x[1]                          # get the encoded data
    icn = icn.replace('#', '\r\n')      # replace...
    icn = icn.replace('%', '=')         # ...some bits first
    icn = base64.b64decode(icn)         # decode
    uxd = uuid.uuid4()                  # create a UUID
    path = 'cached/' + str(uxd) + '.png'
    f = open(path, 'wb')                # save
    f.write(icn)
    f.close()
    return path;

  else:
    print("Invalid icon type: " + x[0])
    return ""



def DecodeRequest(request, result):

  content = request.splitlines()
  #print (content)

  # validate: should start with 'SNP/3.1' and end with 'END'

  if not content[0].startswith('SNP/3.1'):
    return 136,"UnsuportedProtocol"

  elif content[len(content)-1] != 'END':
    return 107,"BadPacket"

  elif len(content) < 3:
    return 132,"NothingToDo"

  else:
    # need to check action is either NOTIFY or FORWARD...


    # we'll check for these afterwards...
    
    title = ""
    text = ""
    
    # process each line...
    for line in content[1:len(content)-1]:
      # split on ': '
      kvp = line.split(': ', 1)

      if kvp[0] == "title":
        title = kvp[1]

      elif kvp[0] == "text":
        text = kvp[1]
        
      elif kvp[0] == "icon":
        # process the icon...
        kvp[1] = decode_icon(kvp[1])
        #print('ICON>>' + kvp[1])

      # store in the dictionary...
      result[kvp[0]] = kvp[1]
        
      #print(kvp[0] + ' --> ' + kvp[1])

    # uncomment to print out the dictionary content...
    #print(result)

    if title == "" and text == "":
      return 109,"ArgMissing"
    

    return 0,""

