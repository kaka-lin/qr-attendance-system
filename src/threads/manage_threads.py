import os

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant

from src.threads.qrcode_thread import QRCodeThread
from src.threads.google_sheet_thread import GoogleSheetThread

ROOT_DIR = os.getcwd()


class ManageThreads(QObject):
    qrcodeGenMsg = pyqtSignal(str, arguments=['genMsg'])

    dumpSig = pyqtSignal(str, str, str, arguments=[
                         'id', 'name', 'email'])
    dumpInit = pyqtSignal()

    def __init__(self, parent=None):
        super(ManageThreads, self).__init__(parent)

        self.__thread_maps = {}

    @pyqtSlot(str, str, str)
    def qrcode_generate(self, data, output_file, output_dir):
        if not output_file:
            output_file = "qrcode.png"
        if not output_dir:
            output_dir = os.path.join(ROOT_DIR, "images")
        
        worker = QRCodeThread()
        thread = QtCore.QThread(self)
        self.__thread_maps['qrcode_generate'] = [thread, worker]
        worker.moveToThread(thread)

        worker.qrcodeGenMsg.connect(self.qrcodeGenMsg)
        worker.qrcodeGenDone.connect(self.onGenDone)

        thread.started.connect(lambda: worker.generate(data, output_file, output_dir))
        thread.start()
    
    @pyqtSlot()
    def onGenDone(self):
        if 'qrcode_generate' in self.__thread_maps:
            thread, worker = self.__thread_maps['qrcode_generate']
            thread.quit()
            thread.wait()
        print("Generate QRCode Thread Finish")

    @pyqtSlot(str, str)
    def get_sheet_data(self, service_file, url):
        self.dumpInit.emit()
        
        worker = GoogleSheetThread(service_file, url)
        thread = QtCore.QThread(self)
        self.__thread_maps['get_sheet_data'] = [thread, worker]
        worker.moveToThread(thread)

        worker.dumpSig.connect(self.dumpSig)
        worker.dumpDone.connect(self.dumpDone)

        thread.started.connect(lambda: worker.get_all_data(0))
        thread.start()

    @pyqtSlot()
    def dumpDone(self):
        if 'get_sheet_data' in self.__thread_maps:
            thread, worker = self.__thread_maps['get_sheet_data']
            thread.quit()
            thread.wait()
        print("Dump Thread Finished")
