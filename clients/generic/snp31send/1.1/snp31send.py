# -*- coding: UTF-8 -*-
import socket
import sys

_verbose = False

# Change Log
#
# V1.1
#	Added: -U (unsubcribe) option
#	Fixed: -S option wasn't including uid parameter
#	Split printHint() and printVerion() out
#
# V1.0
#	Initial release
#

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# printVersion()
#
def printVersion():
    print "snp31send.py V1.1\nCopyright (c) 2017 full phat products"

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Credit: http://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
#
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Helper: print to console if _verbose is True
#
def log(string):
    global _verbose

    if _verbose:
        print string

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Helper: send message and receive response
#
def send_and_receive(ipAddr, port, request):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)

    try:
        log("Connecting to " + ipAddr + ":" + str(port) + "...")
        client.connect((ipAddr, port))

    except socket.timeout:
        log("Timed out!")
        return False, "Connection timed out"

    except Exception as e:
        log("FAILED")
        return False, e

    try:
        log("Sending...")
        client.send(request)
        log("Sent")

    except socket.timeout:
        client.close()
        return False, "Timed out sending request"

    except Exception as e:
        client.close()
        return False, e


    try:
        log("Waiting for reply...")
        reply = client.recv(4096)
        log("Complete!")

    except socket.timeout:
        client.close()
        return False, "Timed out waiting for reply"

    except Exception as e:
        client.close()
        return False, e

    # completed!
    client.close()
    return True, reply


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# printHint()
#
def printHint():
    print "snp31send.py: try 'python snp31send.py --help' for more information"


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# printHelpPage()
#
def printHelpPage():
    print "\nUsage: snp31send.py <host> <port> [options...]"
    print "Options: (F) means FORWARD, (N) NOTIFY, (R) REGISTER, (S) SUBSCRIBE, (U) UNSUBSCRIBE"
    print " -F   Generate FORWARD message"
    print " -N   Generate NOTIFY message"
    print " -R   Generate REGISTER message"
    print " -S   Generate SUBSCRIBE message"
    print " -U   Generate UNSUBSCRIBE message"
    print " -a   application id (R,N)"
    print " -b   notification body (F,N)"
    print " -d   data-* entry (F,N)"
    print " -f   forward-to (F,N,S)"
    print " -i   icon (F,N,R)"
    print " -p   priority (F,N)"
    print " -r   reply port (F,N,S)"
    print " -s   source (F)"
    print " -t   title (F,N,R)"
    print " -u   uid (F,N,S,U)"
    print " -v   Enable verbose mode"
    print " -w   password (F,N,R,S)"
    print " -x   x-* header (F,N)"
    print ""
    print "<host> can be IP address, host name, or '.' (localhost)"

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Helper: splitEntry(string)
#
def splitEntry(string):
    i = string.find(":")
    if i == -1:
        return "",""

    a = string[0:i].strip()
    b = string[i+1:].strip()
    return a,b

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# safeGetEntry(list<string>, int)
#
def safeGetEntry(list, index):
    if index >= 0 and index < len(list):
        return list[index]

    else:
        return ""

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Main()

# strip .py filename
del sys.argv[0]

# help requested?
if len(sys.argv) == 1 and sys.argv[0] == "--help":
    printHelpPage()
    sys.exit()

if len(sys.argv) == 1 and sys.argv[0] == "--version":
    printVersion()
    sys.exit()

# validate args
if len(sys.argv) < 3:
    printHint()
    sys.exit()

# get host
host = sys.argv[0].strip()

# get port
port = 0
try:
    port = int(sys.argv[1])

except:
    port = 0

# validate host and port

if host == ".":
    host = "127.0.0.1"

if host == "":
    print 'Must specify <host> parameter'
    sys.exit()

if (port == 0):
    print 'Must specify <port> parameter'
    sys.exit()


# strip host and port args...
del sys.argv[0]
del sys.argv[0]

action = ""
appId = ""
body = ""
icon = ""
source = ""
title = ""
data = { }
xheader = { }
replyPort = 0
uid = ""
priority = ""
forwardTo = ""
password = ""

for i in range(len(sys.argv)):
    #print str(i) + ":" + sys.argv[i]
    s = sys.argv[i]

    if s == "-N":
        action = "NOTIFY"

    if s == "-R":
        action = "REGISTER"

    if s == "-S":
        action = "SUBSCRIBE"

    if s ==  "-F":
        action = "FORWARD"

    if s ==  "-U":
        action = "UNSUBSCRIBE"

    if s == "-a":
        # app identifier
        i+=1
        appId = safeGetEntry(sys.argv, i);

    if s == "-b":
        # body (text)
        i+=1
        body = safeGetEntry(sys.argv, i);

    if s == "-d":
        # data-*
        i+=1
        d = safeGetEntry(sys.argv, i);
        dataKey,dataValue = splitEntry(d)
        if dataKey != "" and dataValue != "":
            data[dataKey] = dataValue

    if s == "-f":
        # forward-to
        i+=1
        forwardTo = safeGetEntry(sys.argv, i);

    if s == "-i":
        # icon
        i+=1
        icon = safeGetEntry(sys.argv, i);

    if s == "-r":
        # reply port (must be an int > 0)
        i+=1
        portStr = safeGetEntry(sys.argv, i);
        try:
            replyPort = int(portStr)

        except:
            replyPort = 0

    if s == "-p":
        # priority
        i+=1
        priority = safeGetEntry(sys.argv, i);

    if s == "-s":
        # source
        i+=1
        source = safeGetEntry(sys.argv, i);

    if s == "-t":
        # title
        i+=1
        title = safeGetEntry(sys.argv, i);

    if s == "-u":
        # uid
        i+=1
        uid = safeGetEntry(sys.argv, i);

    if s == "-v":
        # verbose
        _verbose = True;

    if s == "-w":
        # password
        i+=1
        password = safeGetEntry(sys.argv, i);

    if s == "-x":
        # x-*
        i+=1
        xh = safeGetEntry(sys.argv, i);
        vh = xh.split(':')
        if len(vh) == 2 and vh[0].strip() != "" and vh[1].strip() != "":
            xheader[vh[0].strip()] = vh[1].strip()

# check we have a valid action...
if action != "NOTIFY" and action != "REGISTER" and action != "SUBSCRIBE" and action != "FORWARD" and action != "UNSUBSCRIBE":
    print "Unknown command (or command missing)"
    printHint()
    sys.exit()

# start building the message...
request = "SNP/3.1 " + action + "\r\n"

# add the action content...
if action == "NOTIFY":
    if appId != "":
        request += "app-id: " + appId + "\r\n"

    if password != "":
        request += "password: " + password + "\r\n"

    if title != "":
        request += "title: " + title + "\r\n"

    if body != "":
        request += "text: " + body + "\r\n"

    if icon != "":
        request += "icon: " + icon + "\r\n"

    if uid != "":
        request += "uid: " + uid + "\r\n"

    if priority != "":
        request += "priority: " + priority + "\r\n"

    if replyPort > 0:
        request += "reply-port: " + str(replyPort) + "\r\n"


    # add data-* entries...
    for key, value in data.iteritems():
        request += "data-" + key + ": " + value + "\r\n"

    # add x-* entries...
    for key, value in xheader.iteritems():
        request += "x-" + key + ": " + value + "\r\n"


elif action == "REGISTER":
    if appId != "":
        request += "app-id: " + appId + "\r\n"

    if title != "":
        request += "title: " + title + "\r\n"

    if icon != "":
        request += "icon: " + icon + "\r\n"

    if password != "":
        request += "password: " + password + "\r\n"


elif action == "FORWARD":
    if source != "":
        request += "source: " + source + "\r\n"

    if password != "":
        request += "password: " + password + "\r\n"

    if title != "":
        request += "title: " + title + "\r\n"

    if body != "":
        request += "text: " + body + "\r\n"

    if icon != "":
        request += "icon: " + icon + "\r\n"

    if priority != "":
        request += "priority: " + priority + "\r\n"

    if uid != "":
        request += "uid: " + uid + "\r\n"

    if replyPort > 0:
        request += "reply-port: " + str(replyPort) + "\r\n"

    # add data-* entries...
    for key, value in data.iteritems():
        request += "data-" + key + ": " + value + "\r\n"

    # add x-* entries...
    for key, value in xheader.iteritems():
        request += "x-" + key + ": " + value + "\r\n"


elif action == "SUBSCRIBE":

    if replyPort > 0:
        request += "reply-port: " + str(replyPort) + "\r\n"

    if uid != "":
        request += "uid: " + uid + "\r\n"

    if forwardTo != "":
        request += "forward-to: " + forwardTo + "\r\n"

    if password != "":
        request += "password: " + password + "\r\n"


elif action == "UNSUBSCRIBE":

    if uid != "":
        request += "uid: " + uid + "\r\n"


request += "END\r\n"

if _verbose:
    print color.BOLD + "["
    print request.strip()
    print "]" + color.END

success,reply = send_and_receive(host, port, request)

if (success):
    print color.BOLD + "["
    print reply.strip()
    print "]" + color.END

else:
    print "FAILED:" + reply

#EOF
