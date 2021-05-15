from dataclasses import dataclass
from datetime import datetime
from json import dumps as json_dumps
from constants import APPLICATION_NAME, APPLICATION_VERSION

@dataclass
class HamlogQSO():

    call            : str
    gridsquare      : str
    mode            : str
    rst_sent        : str
    rst_rcvd        : str
    datetime_on     : datetime
    datetime_off    : datetime
    tx_freq_hz      : int
    mycall          : str
    mygrid          : str
    tx_power        : str           = None
    comments        : str           = None
    name            : str           = None
    operator_call   : str           = None

    def as_adif(self):
        version = f'{(APPLICATION_NAME)} {APPLICATION_VERSION}'
        adif = f'<adif_ver:5>3.1.0<programid:{len(version)}>{version}<EOH>'
        adif += f'<call:{len(self.call)}>{self.call}'
        adif += f'<gridsquare:{len(self.gridsquare)}>{self.gridsquare}'
        if self.mode == 'FT4' or self.mode == 'FST4':
            mode = 'MFSK'
            adif += f'<mode:{len(mode)}>{mode}'
            adif += f'<submode:{len(self.mode)}>{self.mode}'
        else:
            adif += f'<mode:{len(self.mode)}>{self.mode}'
        adif += f'<rst_sent:{len(self.rst_sent)}>{self.rst_sent}'
        adif += f'<rst_rcvd:{len(self.rst_rcvd)}>{self.rst_rcvd}'
        qso_date_on = self.datetime_on.strftime('%Y%m%d')
        adif += f'<qso_date:{len(qso_date_on)}>{qso_date_on}'
        qso_time_on = self.datetime_on.strftime('%H%M%S')
        adif += f'<time_on:{len(qso_time_on)}>{qso_time_on}'
        qso_date_off = self.datetime_off.strftime('%Y%m%d')
        adif += f'<qso_date_off:{len(qso_date_off)}>{qso_date_off}'
        qso_time_off = self.datetime_off.strftime('%H%M%S')
        adif += f'<time_off:{len(qso_time_off)}>{qso_time_off}'
        band = self.band_for_freq(self.tx_freq_hz)
        adif += f'<band:{len(band)}>{band}'
        freq_str = f'{ self.tx_freq_hz / 1e6 :6f}'
        adif += f'<freq:{len(freq_str)}>{freq_str}'
        adif += f'<station_callsign:{len(self.mycall)}>{self.mycall}'
        adif += f'<my_gridsquare:{len(self.mygrid)}>{self.mygrid}'
        if self.tx_power:
            adif += f'<tx_pwr:{len(self.tx_power)}>{self.tx_power}'
        if self.comments:
            adif += f'<comment:{len(self.comments)}>{self.comments}'
        if self.name:
            adif += f'<name:{len(self.name)}>{self.name}'
        if self.operator_call:
            adif += f'<operator:{len(self.operator_call)}>{self.operator_call}'
        adif += '<EOR>'
        return adif

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