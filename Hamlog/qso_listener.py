from asyncio import create_task
from Utils import with_log

@with_log
class QSOListener():

    class ListenerProtocol():

        def __init__(self, callback):
            super().__init__()
            self._callback = callback

        def report_qso(self, qso):
            self._callback(qso)

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self._listener_task = None

    def start(self):
        self.log.debug('Starting listener')

    def stop(self):
        self.log.debug('Stopping listener')
