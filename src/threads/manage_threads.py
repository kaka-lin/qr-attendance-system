import os

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant

from src.threads.qrcode_thread import QRCodeThread
from src.threads.google_sheet_thread import GoogleSheetThread
from src.threads.video_thread import VideoThread


class ManageThreads(QObject):
    genQRCodeSig = pyqtSignal(str, arguments=['image_path'])

    sheetDumpInit = pyqtSignal()
    sheetDumpSig = pyqtSignal(str, str, str, str, arguments=[
        'id', 'chinese_name', 'english_name', 'email'])
    genQRCodeSheetDone = pyqtSignal()

    frameReady = pyqtSignal(np.ndarray)
    finished = pyqtSignal()

    decodeMsgSig = pyqtSignal(str, arguments=['qr_data'])

    def __init__(self, db, parent=None):
        super(ManageThreads, self).__init__(parent)

        self.db = db
        self.__thread_maps = {}

    @pyqtSlot(str, str, str)
    def genQRCode(self, data, output_file, output_dir):
        if not output_file:
            output_file = "qrcode.png"
        if not output_dir:
            root_path = os.environ["ROOT_DIR"]
            output_dir = os.path.join(root_path, "images")
        
        worker = QRCodeThread()
        thread = QtCore.QThread(self)
        self.__thread_maps['generate_qrcode'] = [thread, worker]
        worker.moveToThread(thread)

        worker.genQRCodeSig.connect(self.genQRCodeSig)
        worker.genQRCodeDone.connect(self.onGenQRCodeDone)

        thread.started.connect(lambda: worker.generate(data, output_file, output_dir))
        thread.start()
    
    @pyqtSlot()
    def onGenQRCodeDone(self):
        if 'generate_qrcode' in self.__thread_maps:
            thread, worker = self.__thread_maps['generate_qrcode']
            thread.quit()
            thread.wait()
        print("Generate QRCode Thread Finish")
    
    @pyqtSlot(str, str)
    def genQRCodeSheet(self, service_file, url):
        self.sheetDumpInit.emit()
        
        worker = GoogleSheetThread(service_file, url, self.db)
        thread = QtCore.QThread(self)
        self.__thread_maps['generate_qrcode_sheet'] = [thread, worker]
        worker.moveToThread(thread)

        worker.sheetDumpSig.connect(self.sheetDumpSig)
        worker.genQRCodeSheetDone.connect(self.onGenQRCodeSheetDone)

        thread.started.connect(lambda: worker.generate_code_sheet(0))
        thread.start()
    
    @pyqtSlot()
    def onGenQRCodeSheetDone(self):
        if 'generate_qrcode_sheet' in self.__thread_maps:
            thread, worker = self.__thread_maps['generate_qrcode_sheet']
            thread.quit()
            thread.wait()
        print("Generate QRCode With Sheets Thread Done")
    
    ############################################################################################################
    # The following methods are used to scan the QR code
    @pyqtSlot()
    def opencvStart(self):
        worker = VideoThread()
        thread = QtCore.QThread(self)
        self.__thread_maps['OpenCV'] = [thread, worker]
        worker.moveToThread(thread)

        worker.frameReady.connect(self.frameReady)
        worker.finished.connect(self.finished)
        worker.decodeMsgSig.connect(self.decodeMsgSig)

        thread.started.connect(worker.start)
        thread.start()

    @pyqtSlot()
    def opencvStop(self):
        if 'OpenCV' in self.__thread_maps:
            thread, worker = self.__thread_maps['OpenCV']
            worker.stop()

    @pyqtSlot(str)
    def finished(self, thread_name):
        if thread_name in self.__thread_maps:
            thread, worker = self.__thread_maps[thread_name]
            thread.quit()
            thread.wait()
        print(f"{thread_name} Thread Finished")
