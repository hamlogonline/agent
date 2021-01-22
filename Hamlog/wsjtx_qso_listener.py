from .hamlog_qso import HamlogQSO
from .pywsjtx import WSJTXPacketClassFactory, QSOLoggedPacket, LoggedADIFPacket
from .udp_broadcast_listener import UDPBroadcastQSOListener

class WsjtxQsoListener(UDPBroadcastQSOListener):

    class WsjtxListenerProtocol(UDPBroadcastQSOListener.UDPListenerProtocol):

        def datagram_received(self, data, addr):
            super().datagram_received(data, addr)
            wsjtx_packet = WSJTXPacketClassFactory.from_udp_packet(addr, data)
            if isinstance(wsjtx_packet, LoggedADIFPacket):
                self.log.debug(f'Got WSJT-X ADIF QSO Report: {wsjtx_packet.adif}')
                self.report_adif(wsjtx_packet.adif)
            elif isinstance(wsjtx_packet, QSOLoggedPacket):
                self.log.debug('Got WSJT-X QSO Report')
            

    def __init__(self, callback):
        super().__init__(callback, 2237)
    
    def get_protocol(self):
        return self.WsjtxListenerProtocol(self.callback)
