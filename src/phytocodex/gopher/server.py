from socketserver import TCPServer, StreamRequestHandler
import socket
import systemd.daemon

from ..config import LOGLEVEL
from .handler import GopherHandler


class SocketActivatedServer:
    def __init__(self, _, handler_cls, *args, socket_fd, **kwargs):
        kwargs["bind_and_activate"] = False
        super().__init__(None, handler_cls, *args, **kwargs)
        self.socket = socket.fromfd(
            socket_fd, self.address_family, self.socket_type
        )


class SocketActivatedTCPServer(SocketActivatedServer, TCPServer):
    pass


def main():
    logging.basicConfig(level=LOGLEVEL)
    with SocketActivatedTCPServer(
        None, GopherHandler, socket_fd=systemd.daemon.listen_fds()[0]
    ) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
