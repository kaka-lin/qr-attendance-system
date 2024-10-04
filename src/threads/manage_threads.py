import os

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant

from src.threads.qrcode_thread import QRCodeThread

ROOT_DIR = os.getcwd()


class ManageThreads(QObject):
    qrcodeGenMsg = pyqtSignal(str, arguments=['genMsg'])

    def __init__(self, parent=None):
        super(ManageThreads, self).__init__(parent)

        self.__thread_maps = {}

    @pyqtSlot(str, str, str)
    def generate(self, data, output_file, output_dir):
        if not output_file:
            output_file = "qrcode.png"
        if not output_dir:
            output_dir = os.path.join(ROOT_DIR, "images")
        
        worker = QRCodeThread()
        thread = QtCore.QThread(self)
        self.__thread_maps['generate'] = [thread, worker]
        worker.moveToThread(thread)

        worker.qrcodeGenMsg.connect(self.qrcodeGenMsg)
        worker.qrcodeGenDone.connect(self.onGenDone)

        thread.started.connect(lambda: worker.generate(data, output_file, output_dir))
        thread.start()
    
    @pyqtSlot()
    def onGenDone(self):
        if 'generate' in self.__thread_maps:
            thread, worker = self.__thread_maps['generate']
            thread.quit()
            thread.wait()
        print("Generate QRCode Thread Finish")
