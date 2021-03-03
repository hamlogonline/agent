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

            wsjtx_packet = WSJTXPacketClassFactory.from_udp_packet(addr, data)
            if isinstance(wsjtx_packet, QSOLoggedPacket):
                self.log.debug(f'Got WSJT-X QSO Report, building ADIF')
                datetime_on = datetime.fromtimestamp(wsjtx_packet.timestamp_on)
                qso_date_on = datetime_on.strftime('%Y%m%d')
                qso_time_on = datetime_on.strftime('%H%M%S')
                datetime_off = datetime.fromtimestamp(wsjtx_packet.timestamp_off)
                qso_date_off = datetime_off.strftime('%Y%m%d')
                qso_time_off = datetime_off.strftime('%H%M%S')
                band = self.band_for_freq(wsjtx_packet.tx_freq_hz)
                freq_str = f'{ wsjtx_packet.tx_freq_hz / 1e6 :6f}'
                version = f'{(APPLICATION_NAME)} {APPLICATION_VERSION}'
                adif = f'<adif_ver:5>3.1.0<programid:{len(version)}>{version}<EOH>'
                adif += f'<call:{len(wsjtx_packet.dx_call)}>{wsjtx_packet.dx_call}' 
                adif += f'<gridsquare:{len(wsjtx_packet.dx_grid)}>{wsjtx_packet.dx_grid}'
                if wsjtx_packet.mode == 'FT4' or wsjtx_packet.mode == 'FST4':
                    mode = 'MFSK'
                    adif += f'<mode:{len(mode)}>{mode}'
                    adif += f'<submode:{len(mode)}>{mode}'
                else:
                    adif += f'<mode:{len(wsjtx_packet.mode)}>{wsjtx_packet.mode}'
                adif += f'<rst_sent:{len(wsjtx_packet.rst_sent)}>{wsjtx_packet.rst_sent}'
                adif += f'<rst_rcvd:{len(wsjtx_packet.rst_rcvd)}>{wsjtx_packet.rst_rcvd}'
                adif += f'<qso_date:{len(qso_date_on)}>{qso_date_on}'
                adif += f'<time_on:{len(qso_time_on)}>{qso_time_on}'
                adif += f'<qso_date_off:{len(qso_date_off)}>{qso_date_off}'
                adif += f'<time_off:{len(qso_time_off)}>{qso_time_off}'
                adif += f'<band:{len(band)}>{band}'
                adif += f'<freq:{len(freq_str)}>{freq_str}'
                adif += f'<station_callsign:{len(wsjtx_packet.mycall)}>{wsjtx_packet.mycall}'
                adif += f'<my_gridsquare:{len(wsjtx_packet.mygrid)}>{wsjtx_packet.mygrid}'
                if wsjtx_packet.tx_power:
                    adif += f'<tx_pwr:{len(wsjtx_packet.tx_power)}>{wsjtx_packet.tx_power}'
                if wsjtx_packet.comments:
                    adif += f'<comment:{len(wsjtx_packet.comments)}>{wsjtx_packet.comments}'
                if wsjtx_packet.name:
                    adif += f'<name:{len(wsjtx_packet.name)}>{wsjtx_packet.name}'
                if wsjtx_packet.operator_call:
                    adif += f'<operator:{len(wsjtx_packet.operator_call)}>{wsjtx_packet.operator_call}'
                adif += '<EOR>'
                self.log.debug(f'ADIF: {adif}')
                self.report_adif(adif)
    
        def band_for_freq(self, freq):
            _bands = {
                '2190m':    ( 135700,  		    137800 ),
                '630m':     ( 472000,  		    479000 ),
                '560m':     ( 501000,  		    504000 ),
                '160m':     ( 1800000,   	    2000000 ),
                '80m':      ( 3500000,   	    4000000 ),
                '60m':      ( 5060000,   	    5450000 ),
                '40m':      ( 7000000,   	    7300000 ),
                '30m':      ( 10100000,  	    10150000 ),
                '20m':      ( 14000000,  	    14350000 ),
                '17m':      ( 18068000,  	    18168000 ),
                '15m':      ( 21000000,  	    21450000 ),
                '12m':      ( 24890000,  	    24990000 ),
                '10m':      ( 28000000,  	    29700000 ),
                '8m':  	    ( 40000000,  	    45000000 ),
                '6m':  	    ( 50000000,  	    54000000 ),
                '5m':  	    ( 54000001,  	    69900000 ),
                '4m':  	    ( 70000000,  	    71000000 ),
                '2m':       ( 144000000,        148000000 ),
                '1.25m':    ( 222000000,        225000000 ),
                '70cm':     ( 420000000,        450000000 ),
                '33cm':     ( 902000000,        928000000 ),
                '23cm':     ( 1240000000,       1300000000 ),
                '13cm':     ( 2300000000,       2450000000 ),
                '9cm':      ( 3300000000,       3500000000 ),
                '6cm':      ( 5650000000,       5925000000 ),
                '3cm':      ( 10000000000,      10500000000 ),
                '1.25cm':   ( 24000000000,      24250000000 ),
                '6mm':      ( 47000000000,      47200000000 ),
                '4mm':      ( 75500000000,      81000000000 ),
                '2.5mm':    ( 119980000000,     120020000000 ),
                '2mm':      ( 142000000000,     149000000000 ),
                '1mm':      ( 241000000000,     250000000000 ),
            }
            for band, (freq_min, freq_max) in _bands.items():
                if freq_min <= freq <= freq_max:
                    return band
            else:
                return ''

    def __init__(self, callback):
        super().__init__(callback, application_settings.wsjt_unicast_udp_port)
    
    def get_protocol(self):
        return self.WsjtxListenerProtocol(self.callback)
