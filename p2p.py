
from server_client.constants import *
from server_client.client import Client
from server_client.server import Server


"""
    This class will take care of converting client to server
"""
class p2p:
    # make ourself the default peer
    peers = ['192.168.1.68', '192.168.1.203']
    #peers = ['192.168.1.68']
    #peers = ['127.0.0.1']


def main():
    msg = fileIO.convert_to_bytes()
    while True:
        try:
            print("-" * 21 + "Trying to connect" + "-" * 21)
            # sleep a random time between 1 -5 seconds
           # time.sleep(randint(RAND_TIME_START,RAND_TIME_END))
            for peer in p2p.peers:
                try:
                    client = Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                
                except:
                    pass

                # become the server
                try:
                    server = Server(msg)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass

        except KeyboardInterrupt as e:
            sys.exit(0)

if __name__ == "__main__":
    main()
