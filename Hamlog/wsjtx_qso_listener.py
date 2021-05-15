from .hamlog_qso import HamlogQSO
from .pywsjtx import WSJTXPacketClassFactory, QSOLoggedPacket, LoggedADIFPacket
from .udp_broadcast_listener import UDPBroadcastQSOListener
from datetime import datetime
from constants import APPLICATION_NAME, APPLICATION_VERSION
from settings import application_settings
from socket import socket, AF_INET, SOCK_DGRAM

class WsjtxQsoListener(UDPBroadcastQSOListener):

    class WsjtxListenerProtocol(UDPBroadcastQSOListener.UDPListenerProtocol):

        def __init__(self, port):
            super().__init__(port)
            self._socket = socket(AF_INET, SOCK_DGRAM)

        def repeat_if_needed(self, data):
            if application_settings.wsjt_unicast_udp_repeater_enabled:
                self._socket.sendto(data, (application_settings.wsjt_unicast_udp_repeater_addr, application_settings.wsjt_unicast_udp_repeater_port))

        def datagram_received(self, data, addr):
            super().datagram_received(data, addr)
            self.repeat_if_needed(data)            
            wsjtx_packet = WSJTXPacketClassFactory.from_udp_packet(addr, data)
            if isinstance(wsjtx_packet, QSOLoggedPacket):
                qso = HamlogQSO(
                    wsjtx_packet.dx_call,
                    wsjtx_packet.dx_grid,
                    wsjtx_packet.mode,
                    wsjtx_packet.rst_sent,
                    wsjtx_packet.rst_rcvd,
                    datetime.fromtimestamp(wsjtx_packet.timestamp_on),
                    datetime.fromtimestamp(wsjtx_packet.timestamp_off),
                    wsjtx_packet.tx_freq_hz,
                    wsjtx_packet.mycall,
                    wsjtx_packet.mygrid,
                    wsjtx_packet.tx_power,
                    wsjtx_packet.comments,
                    wsjtx_packet.name,
                    wsjtx_packet.operator_call,
                )
                self.report_adif(qso)

    def __init__(self, callback):
        super().__init__(callback, application_settings.wsjt_unicast_udp_port)
    
    def get_protocol(self):
        return self.WsjtxListenerProtocol(self.callback)
