
# An example script to connect to Google using socket 
# programming in Python 
import socket # for socket 
import sys
from multiprocessing import Process

packetSize = 64

verbose = False
#Use verbose to determine if we should print and log all the info we have
def log(inputString):
	if verbose:
		print(inputString)


class EchoServerAddress:
	#def __init__:...
	name: str
	ip: str
	port: str

serverList = []
address = EchoServerAddress() #Self


#Given the file path to the hostNames list, load in server names and IPs
def ReadHostsFile(hostNamesFilePath):
	file = open(hostNamesFilePath, 'r')

	for line in file:
		#Parse line and load in.
		words = line.split(' ')	
		newServer = EchoServerAddress()
		newServer.name = words[0]
		newServer.ip = words[1]
		newServer.port = words[2]
		serverList.append(newServer)

		#Copy info for self as needed
		if words[0] == address.name:
			address.ip = words[1]
			address.port = words[2]
			#print(newServer.name + words[0] + address.name + address.ip + address.port)

	file.close()



#Open a socket and send
#String param version to avoid using full address info
def SendToName(targetHostName: str, message: str):
	for server in serverList:
		if targetHostName == server.name:
			SendToAddress(server, message)

			#Wait for result?

			return
	print("Error: ", targetHostName, " isn't in the host names file!")

def SendToAddress(targetAddress: EchoServerAddress, message=""):
	try:
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	    print("Socket successfully created")
	except socket.error as err:
	    print("Socket creation failed with error %s" %(err) )
	
	# connecting to the server 
	sock.connect((targetAddress.ip, int(targetAddress.port))) 

	#Add a tag to show origin
	message = address.name + " sent: " + message

	#Send
	print("Sending \"" + message + "\".")
	sock.sendall(bytes(message, 'utf-8'))

	#Listen for the response
	response = str(sock.recv(packetSize), 'utf-8')
	print("Received message: \"" + response + "\".")

	#Done
	sock.close()


#Start the loop to accept messages it will return
def SetUpListening():
	#Set up socket
	print("Setting up socket at " + address.ip + ":" + address.port)
	recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	recvSocket.bind((address.ip, int(address.port)))

	recvSocket.listen(1)
	while True:
		#Wait for a connection
		recvSocket, connectionAddress = recvSocket.accept()

		#Got a message, better copy and send it back
		try:
			#Receive and parse the message
			message = str(recvSocket.recv(packetSize), "utf-8")
			print("Received Message: \"" + message + "\".")
			#origin = message.split(" sent: ")[0]
			message = message.split("sent: ")[1]

			recvSocket.sendall(bytes(address.name + " replies: " + message, 'utf-8'))
			log("Echoed back to " + connectionAddress[0] + ":" + connectionAddress[1])


		finally:
			#Always close once done
			recvSocket.close()

	#Done?
	recvSocket.close()

def SendMessages(message = ""):
	if len(message) == 0:
		print("Input a message to send:")
		message = input()

	#Set up parallel sending processes
	sendingProcesses = []
	for server in serverList:
		if server.name != address.name:
			sendingProcesses.append(Process(target=SendToAddress, args=(server, message)))
	
	#Start those processes
	for sendProcess in sendingProcesses:
		sendProcess.start()
	return sendingProcesses


#Open, prepare for echoing
if __name__ == '__main__':

	#Set self up
	if len(sys.argv) < 2:
		print("What is this server's name?")
		address.name = input()
	else:
		address.name = sys.argv[1]
		print("Set server name to " + sys.argv[1])

	ReadHostsFile("knownhosts.txt")


	listeningProcess = Process(target=SetUpListening)
	listeningProcess.start()

	sendingProcesses = SendMessages()

	#Wait for all to join
	for process in sendingProcesses:
		process.join()
	listeningProcess.join()