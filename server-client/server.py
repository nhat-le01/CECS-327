"""
    This file takes part of the server side of the peer to peer network
    This file deals with uploading of the song for other peers
"""

from server_client.constants import *
SEPARATOR = "<SEPARATOR>"
import os
import tqdm

class Server: 
    def __init__(self, msg):
        try:
            print("Setting up server")
            # the message to upload in bytes
            self.msg = msg

            # define a socket
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Avoid bind() exception: OSError: [Errno 48] Address already in use
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #establish a two-way sockets
            #make another receive sockets
            self.connections = []

            # make a list of peers 
            self.peers = []

            # bind the socket
            self.s.bind((HOST, PORT))

            # listen for connection
            self.s.listen(1)

            print("-" * 12+ "Server Running"+ "-" *21)
            
            self.run()
        except Exception as e:
            sys.exit()



    """
    This method deals with sending info to the clients 
    This methods also closes the connection if the client has left
    :param: connection -> The connection server is connected to 
    :param: a -> (ip address, port) of the system connected
    """
    def handler(self, connection, a):
        
        try:
            while True:
                # server recieves the message
                data = connection.recv(BYTE_SIZE)
                for connection in self.connections:
    
                    # The peer that is connected wants to disconnect
                    if data and data.decode('utf-8')[0].lower() == 'q':

                        # disconnect the peer 
                        self.disconnect(connection, a)
                        return
                    elif data and data.decode('utf-8') == REQUEST_STRING:
                        print("-" * 21 + " UPLOADING " + "-" * 21)
                        print("message ", self.msg)
                        filename = "./data_laptop_1.txt"
                        
                        filesize = os.path.getsize(filename)
                        # if the connection is still active we send it back the data
                        # this part deals with uploading of the file
                        '''
                        connection.send(self.msg)
                        fileIO.create_file(data)
                        '''
                        #send file to client??
                        #convert_to_music(self.msg)

                        connection.send(f"{filename}{SEPARATOR}{filesize}".encode())
                        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                        with open(filename, "rb") as f:
                            while True:
                                bytes_read = f.read(BYTE_SIZE)
                                if not bytes_read:
                                    break
                                self.s.sendall(bytes_read)
                                progress.update(len(bytes_read))

        except Exception as e:
            sys.exit()


    """
        This method is run when the user disconencts
    """
    def disconnect(self, connection, a):
        self.connections.remove(connection)
        self.peers.remove(a)
        connection.close()
        self.send_peers()
        print("{}, disconnected".format(a))
        print("-" * 50)



    """
        This method is use to run the server
        This method creates a different thread for each client
    """
    def run(self):
        # constantly listen for connections
        while True:
            #receive an upcoming connection
            connection, a = self.s.accept()

            # append to the list of peers 
            self.peers.append(a)
            print("Peers are: {}".format(self.peers) )
            self.send_peers() #send a list of peers to all the neighbor nodes
            # create a thread for a connection (handle multiple connections without blocking)
            c_thread = threading.Thread(target=self.handler, args=(connection, a))
            c_thread.daemon = True
            c_thread.start()
            self.connections.append(connection)#add to the list of connections
            print("{}, connected".format(a))
            print("-" * 50)



    """
        send a list of peers to all the peers that are connected to the server
    """
    def send_peers(self):
        peer_list = ""
        for peer in self.peers:
            peer_list = peer_list + str(peer[0]) + ","

        for connection in self.connections:
            # we add a byte '\x11' at the begning of the our byte 
            # This way we can differentiate if we recieved a message or a a list of peers
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, 'utf-8')
            connection.send(PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, 'utf-8'))

