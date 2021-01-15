from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices

def open_url(url_string):
    return QDesktopServices.openUrl(QUrl(url_string))
