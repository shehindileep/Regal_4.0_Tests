""" """
import socket
import traceback
import os
import select
from queue import Queue

from pyDiameter.pyDiaMessage import *
from hss.hss.hss_log import HSSLogMgr
from hss.hss.constants import Constants

avpBuff_res = b'\x01\x00\x06\x28\x40\x00\x01\x3c\x01\x00\x00\x23\x28\x8a\xd7\x51\xd1\xa8\x10\x7f\x00\x00\x01\x07\x40\x00\x00\x28\x6d\x6d\x65\x30\x31\x2e\x6e\x65\x74\x6e\x75\x6d\x62\x65\x72\x2e\x63\x6f\x6d\x3b\x33\x38\x34\x39\x32\x39\x36\x37\x39\x36\x3b\x32\x00\x00\x01\x15\x40\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x01\x08\x40\x00\x00\x1b\x68\x73\x73\x30\x31\x2e\x6e\x65\x74\x6e\x75\x6d\x62\x65\x72\x2e\x63\x6f\x6d\x00\x00\x00\x01\x28\x40\x00\x00\x15\x6e\x65\x74\x6e\x75\x6d\x62\x65\x72\x2e\x63\x6f\x6d\x00\x00\x00\x00\x00\x01\x04\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x02\x40\x00\x00\x0c\x01\x00\x00\x23\x00\x00\x05\x7e\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0b\x00\x00\x01\x0c\x40\x00\x00\x0c\x00\x00\x07\xd1\x00\x00\x01\x29\x40\x00\x00\x20\x00\x00\x01\x0a\x40\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x01\x2a\x40\x00\x00\x0c\x00\x00\x07\xd1\x00\x00\x06\x4e\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x05\x78\xc0\x00\x05\x40\x00\x00\x28\xaf\x00\x00\x05\xd3\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x00\x0d\x80\x00\x00\x0c\x00\x00\x28\xaf\x00\x00\x05\x95\xc0\x00\x01\xfc\x00\x00\x28\xaf\x00\x00\x05\x8f\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x05\x94\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x05\x96\xc0\x00\x01\xd0\x00\x00\x28\xaf\x00\x00\x05\x8f\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x05\xb0\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x01\xed\x40\x00\x00\x1a\x53\x65\x72\x76\x69\x63\x65\x5f\x53\x65\x6c\x65\x63\x74\x69\x6f\x6e\x31\x00\x00\x00\x00\x01\xe6\x40\x00\x00\x68\x00\x00\x01\x4e\x40\x00\x00\x0e\x00\x01\x01\x01\x01\x01\x00\x00\x00\x00\x01\x5c\x40\x00\x00\x30\x00\x00\x01\x1b\x40\x00\x00\x16\x69\x6e\x74\x65\x6c\x6c\x69\x6e\x65\x74\x2e\x63\x6f\x6d\x00\x00\x00\x00\x01\x25\x40\x00\x00\x0f\x73\x65\x72\x76\x65\x72\x41\x00\x00\x00\x00\x7d\x40\x00\x00\x1d\x4d\x49\x50\x36\x5f\x48\x6f\x6d\x65\x5f\x4c\x69\x6e\x6b\x5f\x50\x72\x65\x66\x69\x78\x00\x00\x00\x00\x00\x02\x58\x80\x00\x00\x26\x00\x00\x28\xaf\x56\x69\x73\x69\x74\x65\x64\x5f\x4e\x65\x74\x77\x6f\x72\x6b\x5f\x49\x64\x65\x6e\x74\x69\x66\x69\x65\x72\x00\x00\x00\x00\x05\xc0\xc0\x00\x00\xb8\x00\x00\x28\xaf\x00\x00\x01\xed\x40\x00\x00\x1a\x53\x65\x72\x76\x69\x63\x65\x5f\x53\x65\x6c\x65\x63\x74\x69\x6f\x6e\x31\x00\x00\x00\x00\x01\xe6\x40\x00\x00\x68\x00\x00\x01\x4e\x40\x00\x00\x0e\x00\x01\x01\x01\x01\x01\x00\x00\x00\x00\x01\x5c\x40\x00\x00\x30\x00\x00\x01\x1b\x40\x00\x00\x16\x69\x6e\x74\x65\x6c\x6c\x69\x6e\x65\x74\x2e\x63\x6f\x6d\x00\x00\x00\x00\x01\x25\x40\x00\x00\x0f\x73\x65\x72\x76\x65\x72\x41\x00\x00\x00\x00\x7d\x40\x00\x00\x1d\x4d\x49\x50\x36\x5f\x48\x6f\x6d\x65\x5f\x4c\x69\x6e\x6b\x5f\x50\x72\x65\x66\x69\x78\x00\x00\x00\x00\x00\x02\x58\x80\x00\x00\x26\x00\x00\x28\xaf\x56\x69\x73\x69\x74\x65\x64\x5f\x4e\x65\x74\x77\x6f\x72\x6b\x5f\x49\x64\x65\x6e\x74\x69\x66\x69\x65\x72\x00\x00\x00\x00\x05\x93\xc0\x00\x00\x1e\x00\x00\x28\xaf\x41\x50\x4e\x5f\x4f\x49\x5f\x52\x65\x70\x6c\x61\x63\x65\x6d\x65\x6e\x74\x00\x00\x00\x00\x06\x4d\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x52\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x05\xb2\xc0\x00\x01\xc8\x00\x00\x28\xaf\x00\x00\x05\xb3\xc0\x00\x00\x12\x00\x00\x28\xaf\x40\x41\x61\x32\x34\x56\x00\x00\x00\x00\x05\xb6\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x05\xb7\xc0\x00\x00\x12\x00\x00\x28\xaf\x40\x41\x61\x33\x34\x56\x00\x00\x00\x00\x05\xb9\xc0\x00\x00\x12\x00\x00\x28\xaf\x40\x41\x61\x34\x34\x56\x00\x00\x00\x00\x05\xac\xc0\x00\x00\x12\x00\x00\x28\xaf\x00\x01\x01\x01\x01\x01\x00\x00\x00\x00\x06\x56\x80\x00\x01\x5c\x00\x00\x28\xaf\x00\x00\x06\x57\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x58\x80\x00\x00\xc0\x00\x00\x28\xaf\x00\x00\x06\x44\x80\x00\x00\x20\x00\x00\x28\xaf\x43\x65\x6c\x6c\x5f\x47\x6c\x6f\x62\x61\x6c\x5f\x49\x64\x65\x6e\x74\x69\x74\x79\x00\x00\x06\x42\x80\x00\x00\x28\x00\x00\x28\xaf\x45\x5f\x55\x54\x52\x41\x4e\x5f\x43\x65\x6c\x6c\x5f\x47\x6c\x6f\x62\x61\x6c\x5f\x49\x64\x65\x6e\x74\x69\x74\x79\x00\x00\x06\x45\x80\x00\x00\x21\x00\x00\x28\xaf\x52\x6f\x75\x74\x69\x6e\x67\x5f\x41\x72\x65\x61\x5f\x49\x64\x65\x6e\x74\x69\x74\x79\x00\x00\x00\x00\x00\x06\x46\x80\x00\x00\x22\x00\x00\x28\xaf\x4c\x6f\x63\x61\x74\x69\x6f\x6e\x5f\x41\x72\x65\x61\x5f\x49\x64\x65\x6e\x74\x69\x74\x79\x00\x00\x00\x00\x06\x43\x80\x00\x00\x22\x00\x00\x28\xaf\x54\x72\x61\x63\x6b\x69\x6e\x67\x5f\x41\x72\x65\x61\x5f\x49\x64\x65\x6e\x74\x69\x74\x79\x00\x00\x00\x00\x06\x59\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x06\x5a\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x06\x5b\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x5c\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x5d\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x06\x5e\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x06\x5f\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x60\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x05\xbb\xc0\x00\x00\xe8\x00\x00\x28\xaf\x00\x00\x05\xbc\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x05\xbd\xc0\x00\x00\xcc\x00\x00\x28\xaf\x00\x00\x05\x8f\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x05\xbe\xc0\x00\x00\x12\x00\x00\x28\xaf\x40\x41\x61\x36\x34\x56\x00\x00\x00\x00\x05\x7c\xc0\x00\x00\x12\x00\x00\x28\xaf\x40\x41\x61\x37\x34\x56\x00\x00\x00\x00\x01\xed\x40\x00\x00\x0e\x40\x41\x61\x38\x34\x56\x00\x00\x00\x00\x06\x54\x80\x00\x00\x18\x00\x00\x28\xaf\x45\x78\x74\x5f\x50\x44\x50\x5f\x54\x79\x70\x65\x00\x00\x06\x55\x80\x00\x00\x12\x00\x00\x28\xaf\x00\x01\x01\x01\x01\x01\x00\x00\x00\x00\x05\x9b\xc0\x00\x00\x2c\x00\x00\x28\xaf\x00\x00\x02\x04\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x01\x00\x00\x02\x03\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x01\x00\x00\x06\x4d\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x52\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x05\x9c\xc0\x00\x00\x1c\x00\x00\x28\xaf\x00\x00\x05\x9d\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x01\x00\x00\x06\x53\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x01\x00\x00\x06\x50\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x0a\x00\x00\x06\x51\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x61\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x06\x62\x80\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x00'

class TcpServer:
    """ Class to handle TCPServer """
    def __init__(self):
        self._log = HSSLogMgr("TcpServer").get_logger()
        self._log.debug(">")
        self.regal_root_path = os.getenv("REGAL_ROOT_PATH")
        self._msg_len = 692
        self._buffer_data = b''

        if not self.regal_root_path:
            host_ip = Constants.HOST_IP
            self._server_addr = (host_ip, Constants.HSS_PORT)
            self._log.debug("<")
        else:
            server_addr = Constants.HOST_IP
            self._server_addr = (server_addr, Constants.HSS_PORT)
            self._log.debug("<")
        self._run = True
        self._received = 0
        self._response = 0
        self._log.debug("<")


    def get_status(self):
        """ Method return the total recevied and sent messages

        Returns:
            integer: sent and recevied messages count.

        """
        self._log.debug(">")
        self._log.debug(" %s<", socket.gethostname())
        #return self._response, self._received, socket.gethostbyname()
        self._log.debug("The response %s and recv %s, %s",self._response,
                self._received, socket.gethostname())
        return self._response, self._received, socket.gethostname()

    def reset_counter(self):
        """ Method reset the recv and send messages count to 0

        Returns:
            None

        """
        self._log.debug(">")
        self._response = 0
        self._received = 0
        self._log.debug("Successfully reseted response %s and recv %s %s",
                self._response, self._received, socket.gethostname())
        self._log.debug("<")
        return socket.gethostname()

    def create_and_get_server_socket(self, address):
        """ Method create the server socket

        Args:
            address(tuple): tuple of server and port

        Returns:
            obj: Server socket object

        """
        self._log.debug(">")
        self._log.debug("Creating server socket with address %s", address)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(address)
        server_socket.listen(128)
        server_socket.setblocking(0)
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._log.debug("Successfully created server socket with address %s", address)
        self._log.debug("<")
        return server_socket

    def register_and_get_epoll(self, fileno, epoll_type):
        """ Method to create the epool object and register the epoll events

        Args:
            fileno(int): event
            epoll_type(str): Type of the epoll event

        Returns:
            obj: epoll object

        """
        self._log.debug(">")
        epoll_obj = select.epoll()
        epoll_obj.register(fileno, epoll_type)
        self._log.debug("registered the file fd %s with type %s in epoll"\
                        " object", fileno, epoll_type)
        self._log.debug("<")
        return epoll_obj

    def init_connection(self, fd_link, socket_obj, msg_queue, epoll):
        """Method to initialize a connection with clients.

        Args:
            fd_link(int): ioh
            socket_obj(obj): server socket object
            msg_queue(qdict): message queue
            epoll(obj): epoll object

        Returns:
            None

        """
        self._log.debug(">")
        connection, address = socket_obj.accept()
        connection.setblocking(0)

        fileno = connection.fileno()
        epoll.register(fileno, select.EPOLLIN)
        fd_link[fileno] = connection
        msg_queue[connection] = Queue()
        self._log.debug("<")

    def receive_request(self, fileno, socket_obj, epoll, msg_queue, fd_link):
        """Receive a request and add a response to send.
        Handle client closing the connection.

        Args:
            fileno:
            socket_obj:
            epoll(obj): epoll obeject
            msg_queue(dict): messages dict
            fd_link(dict):

        Returns:
            None

        """
        self._log.debug(">")
        done = True
        while done:
            try:
                data = socket_obj.recv(1024)
            except BlockingIOError as ex:
                break

            if not data:
                socket_obj.close()
                del fd_link[fileno], msg_queue[socket_obj]
                self._log.debug("<")
                break

            self._buffer_data = self._buffer_data + data
            while True:
                if len(self._buffer_data) < self._msg_len:
                    self._log.debug("<")
                    break
                message = self._buffer_data[:self._msg_len]
                self._buffer_data = self._buffer_data[self._msg_len:]
                decode_msg = self.decode_msg(message)
                msg_queue[socket_obj].put(decode_msg)
                self._received = self._received + 1
                self._log.debug("received %s", self._received)
                socket_obj.sendall(decode_msg)
                self._response = self._response + 1
                self._log.debug("sent %s", self._response)
                #epoll.modify(fileno, select.EPOLLOUT)
                done = False
            self._log.debug("<")

    def close_connection(self, fileno, fd_link, epoll):
        """ Method closen the connection with client.

        Args:
            fileno:
            fd_link:
            epoll:

        Returns:
            None

        """
        self._log.debug(">")
        epoll.unregister(fileno)
        fd_link[fileno].close()
        self._log.debug("<")
        del fd_link[fileno]

    def send_response(self, fileno, socket_obj, epoll, msg_queue):
        """Send a response to a client.

        Args:
            fileno:
            socket_obj:
            epoll:
            msg_queue:

        Returns:
            None

        """
        self._log.debug(">")
        try:
            msg = msg_queue[socket_obj].get(False)
        except queue.Empty:
            self._log.debug("<")
            epoll.modify(fileno, select.EPOLLIN)
        else:
            epoll.modify(fileno, select.EPOLLIN)
            socket_obj.sendall(msg)
            self._log.debug("Sending message back to the client "\
                            " %s", socket_obj.getpeername())
            self._log.debug("<")

    def decode_msg(self, encoded_msg):
        """ Method decode the encoded message recevied from the client

        Args:
            encoded_msg(str): Encoded message from the client

        Returns:
            str: decoded ula message

        """
        self._log.debug(">")
        if not encoded_msg:
            self._log.debug("<")
            return " "
        response=DiaMessage()
        response.decode(encoded_msg)

        resp=DiaMessage()
        resp.decode(avpBuff_res)
        resp.setE2EID(response.getE2EID())
        resp.setHBHID(response.getHBHID())

        response_encoded = resp.encode()
        self._log.debug("<")
        return response_encoded

    def run(self):
        """ Method run server. """
        self._log.debug(">")
        try:
            server_obj = self.create_and_get_server_socket(self._server_addr)
            epoll_obj = self.register_and_get_epoll(server_obj.fileno(), select.EPOLLIN)

            fd_link = {
                server_obj.fileno(): server_obj
            }
            msg_queue = {}
            print("Listening")

            while self._run:
                events = epoll_obj.poll(1)
                for fileno, event in events:
                    socket_obj = fd_link[fileno]
                    if socket_obj == server_obj:
                        self.init_connection(fd_link, socket_obj, msg_queue, epoll_obj)
                    elif event & select.EPOLLIN:
                        self.receive_request(fileno, socket_obj, epoll_obj, msg_queue,
                                fd_link)
                        self._log.debug("received %s", self._received)
                    elif event & select.EPOLLOUT:
                        self.send_response(fileno, socket_obj, epoll_obj, msg_queue)
                        self._log.debug("sent %s", self._response)
                    elif event & select.EPOLLHUP:
                        self.close_connection(fileno, fd_link, epoll_obj)
        except Exception as ex:
            self._log.error("Exception: %s", ex)
            self._log.error("Trace back: %s", traceback.format_exc())
            self._log.debug("<")
        except KeyboardInterrupt:
            self.stop()
            self._log.debug("<")
        finally:
            epoll_obj.unregister(server_obj.fileno())
            epoll_obj.close()
            server_obj.close()
            self._log.debug("<")

    def stop(self):
        """ method stop the server """
        self._log.debug(">")
        self._run = False
        self._log.debug("<")

if __name__ == "__main__":
    obj = TcpServer()
    obj.run()
