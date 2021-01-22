from asyncio import get_running_loop
from Utils import with_log
from .qso_listener import QSOListener

class UDPBroadcastQSOListener(QSOListener):

    @with_log
    class UDPListenerProtocol(QSOListener.ListenerProtocol):

        def __init__(self, callback):
            super().__init__(callback)

        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            self.log.debug('Datagram received')

    def __init__(self, callback, port):
        super().__init__(callback)
        self.port = port
        self.transport = None

    async def start(self):
        super().start()
        loop = get_running_loop()
        self.transport, _ = await loop.create_datagram_endpoint(self.get_protocol, local_addr=('127.0.0.1', self.port))

    def stop(self):
        super().stop()
        self.transport.close()

    def get_protocol(self):
        return self.ListenerProtocol(self.callback)
