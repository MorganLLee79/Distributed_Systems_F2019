
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
address = EchoServerAddress #Self


#Given the file path to the hostNames list, load in server names and IPs
def ReadHostsFile(hostNamesFilePath):
	file = open(hostNamesFilePath, 'r')

	for line in file:
		#Parse line and load in.
		words = line.split(' ')	
		newServer = EchoServerAddress
		newServer.name = words[0]
		newServer.ip = words[1]
		newServer.port = words[2]
		serverList.append(newServer)

		#Copy info for self as needed
		if newServer.name = address.name:
			address.ip = newServer.ip
			address.port = newServer.port

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

def SendToAddress(targetAddress: EchoServerAddress):  
	try: 
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	    print("Socket successfully created")
	except socket.error as err:
	    print("socket creation failed with error %s" %(err) )
	
	# connecting to the server 
	sock.connect((targetAddress.ip, targetAddress.port)) 
	
	#Collect what we should send for echo
	if not message:
		print("Input a message to be send out then echoed.")
		message = input()

	#Add a tag to show origin
	message = address.name + " sent: " + message

	#Send
	sock.sendall(message)

	#Listen for the response
	response = sock.recv(packetSize)
	print "Received message: " + response

	#Done
	sock.close()


#Start the loop to accept messages it will return
def SetUpListening():
	#Set up socket
	recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	recvSocket.bind((address.ip, address.port))

	recvSocket.listen(1)
	while True:
		#Wait for a connection
		connectionSocket, connectionAddress = recvSocket.accept()

		#Got a message, better copy and send it back
		try:
			#Receive and parse the message
			message = data.recv(packetSize)
			print("Received Message: " + message)
			message = message.split("sent: ")[2]

			connection.sendall(address.name + " replies: " + message)
			log("Echoed back to " + connectionAddress)


		finally:
			#Always close once done
			connectionSocket.close()

	#Done?
	recvSocket.close()


#Open, prepare for echoing
if __name__ == '__main__':

	#Set self up
	print("What is this server's name?")
	address.name = input()
	ReadHostsFile("knownhosts.txt")
	listeningProcess = Process(target=SetUpListening())
	listeningProcess.start()

	sendingProcesses = []
	for server in serverList:
		sendingProcesses.append(Process(target=SendToAddress(server)))
		sendingProcesses[len(sendingProcess) - 1].start()

	#Wait for all to join
	for process in sendingProcesses:
		process.join()
	listeningProcess.join()