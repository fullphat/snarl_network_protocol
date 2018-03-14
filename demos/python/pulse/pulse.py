#
# Snarl Sample Code
#
# full phat products
#
# PROVIDED WITHOUT WARRANTY OF ANY SORT.  This is sample code to demonstrate
# a concept that may be used without restriction.
#
# Pulse - a network ping for Snarl
#
# When run, this example will ask for the IP address (or hostname) and port
# number of a target machine running Snarl, and the frequency (in minutes)
# to send a regular notification.
#
# Although simplistic, this example demonstrates how applications can
# register with Snarl across a network.  Taken further, this example could
# be used as a rudimentary way to monitor the availability of servers in an
# enterprise.  The fact it's written in Python makes it highly portable
# across different operating systems and architectures.
#

from time import sleep
from random import randint
import socket

#
# Simple SNP3.1 wrapper.  Sends 'packet' to 'ip:port' using SNP3.1
# Returns a (bool,string) tuple.  First element will be True on success; 
# False if a network connection occurred.  If the packet was sent, the
# second element contains the SNP3.1 response received.
#
def snp31send(packet, ip, port):
	hap = ip + ":" + str(port)
	socket.setdefaulttimeout(3)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((ip, port))

	except socket.error as e:
		print "Failed to connect to " + hap + ": " + str(e) 
		return False, ""

	else:
		s.send(packet)
		data = s.recv(2048)
		s.close()
		return True, str(data)



raw_target = raw_input("Destination host name or IP [localhost]: ")
raw_port = raw_input("Destination host port [9887]: ")
raw_delay = raw_input("Number of minutes between each pulse [5]: ")

# get target...

target = raw_target



# get port...

port = 9887
if raw_port != "":
	try:
		port = int(raw_port)

	except:
		port = 0

if port < 1 or port > 65535:
	print "Error: Port must be between 1 and 65535!"
	print ""
	exit()

# get delay...

delay = 5
if (raw_delay) != "":
	try:
		delay = int(raw_delay)

	except:
		delay = 0

if delay < 5:
	print "Error: Delay must be an integer larger than 4!"
	print ""
	exit()

# use this in messages...
target_and_port = target + ":" + str(port)

# generate small variation against minutes delay
print "Generating delay variation..."
delay = delay + randint(-2, 2)
print "Will generate a pulse every " + str(delay) + " minute(s) to " + target_and_port + "..."

# register with Snarl...
print "Registering with Snarl on " + target_and_port + "..."
pRegister = "SNP/3.1 REGISTER\r\napp-id: net.fullphat.pulse_demo\r\ntitle: Pulse Demo\r\nEND\r\n"

result,data = snp31send(pRegister, target, port)
if not result:
	print "Error: failed to register with Snarl: "
	print data
	exit()

print "Registered ok"
print "Running..."

# run!
while 1:
	print("Sending pulse...")

#
	pNotify = "SNP/3.1 NOTIFY\r\n"
	pNotify += "app-id: net.fullphat.pulse_demo\r\n"
	pNotify += "title: Checking in from " + socket.gethostname() + "\r\n"
	pNotify += "icon: !system-info\r\n"
	#pNotify += "text: " + socket.gethostname() + "\r\n"
	pNotify += "END\r\n"
	snp31send(pNotify, target, port)
	sleep(delay * 60)

