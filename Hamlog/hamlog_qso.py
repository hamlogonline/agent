from dataclasses import dataclass, asdict
from datetime import datetime
from json import dumps as json_dumps

@dataclass
class HamlogQSO():

    mycall          : str
    call            : str
    band            : str
    mode            : str
    timestamp_off   : int
    snt             : str
    rcv             : str

    timestamp_on    : int
    contestname     : str = None
    contestnr       : str = None
    rxfreq          : str = None
    txfreq          : str = None
    operator        : str = None
    countryprefix   : str = None
    wpxprefix       : str = None
    stationprefix   : str = None
    continent       : str = None
    sntnr           : int = None
    rcvnr           : str = None
    gridsquare      : str = None
    exchangel       : str = None
    section         : str = None
    comment         : str = None
    qth             : str = None
    name            : str = None
    power           : str = None
    misctext        : str = None
    zone            : str = None
