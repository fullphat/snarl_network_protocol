
import urllib.request
import subprocess
import base64
import uuid
import sys
import os


"""
  bool download_icon(str url)

  Saves the icon pointed to in 'url' to './cached/x.png' (where 'x' is a UUID)
  Returns the path to the saved file

"""
def download_icon(url):
  # download and save to cache...
  uxd = uuid.uuid4()
  path = 'cached/' + str(uxd) + '.png'

  try:
    urllib.request.urlretrieve(url, path)
    return path

  except Exception as downloadError:
    print("Couldn't download: " + url)
    print(downloadError)
    return ""


"""
  bool translate_stock_icon(str name)

  Translates the name of a stock icon into a local file path

"""
def translate_stock_icon(name):
  return os.getcwd() + '/icons/' + name + '.png'


"""
  bool decode_phat64(str data)

  Saves hex-encoded phat64 in 'data' to './cached/x.png' (where 'x' is a UUID)
  Returns the path to the saved file

"""
def decode_phat64(data):
  # decode and save to cache...
  data = data.replace('#', '\r\n')      # replace...
  data = data.replace('%', '=')         # ...some bits first
  data = base64.b64decode(data)         # decode
  uxd = uuid.uuid4()                    # create a UUID
  path = 'cached/' + str(uxd) + '.png'
  f = open(path, 'wb')                  # save
  f.write(data)
  f.close()
  return path


"""
  Tuple<bool,string> is_prefixed_icon(str data)

  Determines if 'data' is a V47 prefixed icon and, if so, decodes it/saves it
  accordingly and returns True and a path to the icon.  If it isn't a valid
  prefixed icon, returns False and "".

"""
def is_prefixed_icon(data):
  allowed = [ "stock", "file", "phat64", "url" ]
  # split on ':'
  kvp = data.split(':', 1)
  if kvp[0] in allowed:
    if kvp[0] == 'stock':
      path = translate_stock_icon(kvp[1])

    elif kvp[0] == 'file':
      path = kvp[1]

    elif kvp[0] == 'phat64':
      path = decode_phat_64(kvp[1])

    elif kvp[0] == 'url':
      path = download_icon(kvp[1])
  
    return True, path

  else:
    return False, ""


"""
    bool decode_icon(str suffix, str data)


"""

def decode_icon(suffix, data):

  if suffix == "":
    return ""

  # decode based on suffix...

  if suffix == 'stock':
    return translate_stock_icon(data)

  elif suffix == 'file':
    # assume local
    return data

  elif suffix == 'url':
    return download_icon(data)

  elif suffix == 'phat64':
    return decode_phat64(data)

  else:
    print("Invalid icon type: " + suffix)
    return ""


"""
    <int,string> DecodeRequest(str request, dict result)

    "request" should be a complete SNP 3.1 request, including header and footer.  On successful
    decoding, this function returns True and populates "result" with 'title', 'text' and 'icon'
    if these elements are provided.

    Currently only supports the SNP 3.1 NOTIFY command.

    Will decode phat64 encoded icons.  Saves them to the working folder as '<UUID>.png' and
    sets result['icon'] to the path.

"""

def DecodeRequest(request, result):

  content = request.splitlines()
  #print (content)

  # check footer

  if content[len(content)-1] != 'END':
    return 107,"BadPacket"

  # check we have something...

  if len(content) < 3:
    return 132,"NothingToDo"

  # check header and get command...

  cmd = DecodeHeader(content[0])  
  if cmd != "NOTIFY" and cmd != "FORWARD":
    return 112,"NotImplemented"

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
        b,s = is_prefixed_icon(kvp[1])
        if b:
          kvp[1] = s
        
        #kvp[1] = decode_icon(kvp[1])
        print('ICON>>' + kvp[1])

      elif kvp[0] == "icon-phat64":
        kvp[0] = "icon"
        kvp[1] = decode_icon("phat64", kvp[1])

      elif kvp[0] == "icon-url":
        kvp[0] = "icon"
        kvp[1] = decode_icon("url", kvp[1])

      # store in the dictionary...
      result[kvp[0]] = kvp[1]
        
      #print(kvp[0] + ' --> ' + kvp[1])

    # uncomment to print out the dictionary content...
    #print(result)

    if title == "" and text == "":
      return 109,"ArgMissing"
    

    return 0,""

"""
    <string> DecodeHeader(string header)

    Attempts to decode header.  Returns the SNP 3.1 command or an empty string
    if the header is invalid

"""

def DecodeHeader(header):

  # should start with 'SNP/3.1'...

  if not header.startswith('SNP/3.1'):
    return 136,"UnsuportedProtocol"

  # get command (should be second item after splitting on a single space...)

  s = header.split(' ', 1)
  if len(s) < 2:
    return 136,"UnsuportedProtocol"

  return s[1];
    return 130,"InvalidHeader"


