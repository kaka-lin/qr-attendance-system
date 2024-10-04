import os

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant

from src.app.qrcode_helper import QRCodeHelper


class QRCodeThread(QObject):
    qrcodeGenMsg = pyqtSignal(str)
    qrcodeGenDone = pyqtSignal()

    def __init__(self, parent=None):
        super(QRCodeThread, self).__init__(parent)

        self.qrcode = QRCodeHelper()

    @pyqtSlot(str, str, str)
    def generate(self, data, output_file, output_dir):
        """ Generate QRCode Thread Start """
        print("Generate QRCode Thread Start")
        image_path = self.qrcode.generate(data, output_file=output_file, output_dir=output_dir)
        self.qrcodeGenMsg.emit(image_path)
        self.qrcodeGenDone.emit()
