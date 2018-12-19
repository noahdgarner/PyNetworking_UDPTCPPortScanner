#Noah D Garner
#Python PRogram implementing client side chat room
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.connect((IP_address, Port))
server.send('HELLO')
server_data = server.recv(1024)
print str(server_data)

auth = "AUTHNO"
attempts = 0
sockets_list = [0, server]
list_clients_db = [('garner','p926'),('test1','p001'),('test2','p002'),('test3','003')]

while (1):
	usern = raw_input("Please enter the username!: ")
	passw = raw_input("Please enter the password!: ")
	server.send('AUTH:'+usern+':'+passw)
	auth = server.recv(1024)
	print auth
	if len(str(auth)) == 6:
	    attempts = attempts + 1
	    print "Invalid, please re enter info."
	    if (attempts >= 3):
		print 'You need to use one of these to log in: %s'% (list_clients_db)
	else:
	    break

print "You are now authenticated"


login = 1



while (login):
	print "Choose an option:\n 1. List online users \n 2. Send someone a message \n 3. Sign Off \n"

	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	for socks in read_sockets: 
		if socks == server: 
		    message = socks.recv(1024)
		    print message
		else: 
		    message = sys.stdin.readline().rstrip('\r\n') #take standard in then strip the terminating char
		   
		    if message is '1':
			server.send(str.encode('LIST'))
			print "Printing list of users"
		    elif message is '2':
			otheruser = raw_input("Whart user do you want to message: ")
			msg = raw_input("Message: ")
			server.send(str.encode("TO:"+otheruser+":"+msg))
			print "Message sent"
		    else:
			login = 0
			server.send(str.encode("BYE"))
			print "Leaving Goodbye."
	




server.close()









