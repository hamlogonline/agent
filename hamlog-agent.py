#!/usr/bin/env python

""" hamlog-agent: desktop agent software for Hamlog online logging platform """

# Workaround for maxOS Big Sur
import os
os.environ["QT_MAC_WANTS_LAYER"] = "1"
# end of the workaround

from os import name as os_name
from sys import exit as sys_exit, argv as sys_argv
from PySide2.QtCore import QCoreApplication, QEvent, QSettings, QUrl, QTextStream, QThread, QStandardPaths
from PySide2.QtGui import QFileOpenEvent
from PySide2.QtWidgets import QApplication
from PySide2.QtNetwork import QLocalServer, QLocalSocket
from qasync import QEventLoop
from asyncio import set_event_loop, create_task
from pathlib import Path
from logging import FileHandler, Formatter as LogFormatter, getLogger

from constants import APPLICATION_NAME, APPLICATION_ORGANIZATION_NAME, APPLICATION_ORGANIZATION_DOMAIN, APPLICATION_LOG_FILE_NAME, APPLICATION_LOG_FORMAT, APPLICATION_LOG_LEVEL
from UI import MainWindow
from Hamlog import hamlog
from Utils import with_log

@with_log
class HamlogAgentApplication(QApplication):

    activation_window = None

    def __init__(self, app_id, scheme_url):
        super().__init__()
        self._app_id = app_id
        self._socket = QLocalSocket()
        self._socket.connectToServer(self._app_id)
        self._is_running = self._socket.waitForConnected()
        if self._is_running:
            self._out_stream = QTextStream(self._socket)
            self._out_stream.setCodec('UTF-8')
            if scheme_url:
                self.log.debug('Sending scheme URL notification')
                self._out_stream << scheme_url
                self._out_stream.flush()
                self._socket.waitForBytesWritten()
        else:
            self._socket = None
            self._in_socket = None
            self._in_stream = None
            self._server = QLocalServer()
            self._server.listen(self._app_id)
            self._server.newConnection.connect(self._on_new_connection)

    def _on_new_connection(self):
        if self._in_socket:
            self._in_socket.readyRead.disconnect(self._on_ready_read)
        self._in_socket = self._server.nextPendingConnection()
        if not self._in_socket:
            return
        self._in_stream = QTextStream(self._in_socket)
        self._in_stream.setCodec('UTF-8')
        self._in_socket.readyRead.connect(self._on_ready_read)
        self._activate()
    
    def _activate(self):
        if self.activation_window:
            self.activation_window.show()

    def _on_ready_read(self):
        message = self._in_stream.readLine()
        self._in_socket.close()
        hamlog.process_url_scheme(message.lower())

    def is_running(self):
        return self._is_running

    def event(self, ev):
        if ev.type() == QEvent.FileOpen:
            return hamlog.process_url_scheme(ev.url().toString())
        else:
            return super().event(ev)

    def register_url_scheme(self):
        if os_name == 'nt':
            try:
                from sys import frozen as application_frozen
                if application_frozen:
                    from sys import executable as executable_path
                    registry_classes_path = 'HKEY_CURRENT_USER\\SOFTWARE\\Classes'
                    hamlog_agent_key = QSettings(registry_classes_path + '\\hamlogagent', QSettings.NativeFormat)
                    hamlog_agent_key.setValue('.', 'HAMLOG Agent')
                    hamlog_agent_key.setValue('URL Protocol', '')
                    hamlog_agent_open_key = QSettings(registry_classes_path + '\\hamlogagent\\shell\\open\\command', QSettings.NativeFormat)
                    hamlog_agent_open_key.setValue('.', f'"{executable_path}" "%1"')
            except:
                pass

if __name__ == '__main__':
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    QCoreApplication.setOrganizationName(APPLICATION_ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(APPLICATION_ORGANIZATION_DOMAIN)

    # Set up logging
    logging_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    Path(logging_dir).mkdir(parents=True, exist_ok=True)
    logging_handler = FileHandler(Path(logging_dir).joinpath(APPLICATION_LOG_FILE_NAME))
    logging_handler.setFormatter(LogFormatter(APPLICATION_LOG_FORMAT))
    logger = getLogger()
    logger.addHandler(logging_handler)
    logger.setLevel(APPLICATION_LOG_LEVEL)

    try:
        scheme_url = sys_argv[1]
    except:
        scheme_url = None
    application = HamlogAgentApplication(APPLICATION_ORGANIZATION_DOMAIN, scheme_url)
    if application.is_running():
        sys_exit(0)
    application.register_url_scheme()
    event_loop = QEventLoop(application)
    set_event_loop(event_loop)
    main_window = MainWindow.get_shared_instance()
    application.activation_window = main_window
    main_window.show()
    if os_name == 'nt':
        try:
            file_open_event = QFileOpenEvent(QUrl(scheme_url))
            application.sendEvent(application, file_open_event)
        except IndexError:
            pass
    create_task(hamlog.start_listeners())
    with event_loop:
        sys_exit(event_loop.run_forever())
