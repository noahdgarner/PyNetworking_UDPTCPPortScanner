# Noah D Garner
# Simple Chatroom, server side
# 11/24/2018
import socket 
import select 
import sys 
from thread import *
  

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print "Correct usage: script, IP address, port number"
    exit() 
  
# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 
  
# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 
  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters ls
"""
server.bind((IP_address, Port)) 
  
server.listen(100) 
  
list_of_clients = []
list_of_users = [] 
list_clients_db = [('garner','p926'),('test1','p001'),('test2','p002'),('test3','003')]

def clientthread(conn, addr): 
  
    # sends a message to the client whose user object is conn 
    while True: 
            try: 
		    data = conn.recv(1024)
		    if data:
		        #parse and determine what they sent
		        if 'HELLO' in data:
			    print str(data)
		            conn.send("HELLO")
		            while True:
		                auth = conn.recv(1024)
		                if 'AUTH' in auth:
		                    auth, user, pw = auth.decode().split(":")
				    if (user,pw) in list_clients_db:
		                        print(user, " logged in")
		                        list_of_users.append((user, conn))
		                        conn.send("AUTHYES")
		                        signMsg = "SIGNIN:" + user
		                        conn.send(signMsg)
		                        break
				    else:
					conn.send("AUTHNO")
		                else:
				    conn.send("AUTHNO")
			elif 'LIST' in data:
			    users = ""
			    for u, c in list_of_users:
				users = u+", "+ users
			    print users
			    conn.send(users)
			elif 'BYE' in data:
			    print user+" signed off"
			    signMsg = "SIGNOFF:"+user
			    broadcast(signMsg, server)
			    remove(user)
			    conn.close()
			elif 'TO' in data:
			    to, toUser, userMsg = data.decode().split(":")
			    print "sending msg from " + user + " to " + toUser
			    userMsg = "FROM:" + user + ":" + userMsg
			    for (u, c) in list_of_users:
				if u==toUser:
				     c.send(userMsg)

		    else: 
                        remove(conn) 
			list_of_users.remove((user, conn))
  
            except: 
                continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
    print list_of_clients
    for clients in list_of_clients:
        try: 
	    print message
            clients.send(str.encode(message)) 
	    print message
        except: 
            clients.close() 
  
            # if the link is broken, we remove the client 
            remove(clients) 
  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept() 
  
    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append(conn) 
  
    # prints the address of the user that just connected 
    print addr[0] + " connected"
  
    # creates and individual thread for every user  
    # that connects 
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 

