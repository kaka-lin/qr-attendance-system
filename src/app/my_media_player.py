import sys

import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, pyqtProperty, QSize, QByteArray
from PyQt5.QtGui import QImage
from PyQt5.QtMultimedia import QAbstractVideoSurface, QVideoFrame, QVideoSurfaceFormat


class MyMediaPlayer(QObject):
    surfaceChanged = pyqtSignal(QAbstractVideoSurface)

    def __init__(self, manage_thread, parent=None):
        super(MyMediaPlayer, self).__init__(parent)

        self.m_surface = None
        self.m_format = QVideoSurfaceFormat()
        self.m_isFormatSet = False
        self.m_image = None

        self.m_backend = manage_thread
        self.m_backend.frameReady.connect(self.onVideoFrameReady)
    
    @pyqtProperty(QAbstractVideoSurface, notify=surfaceChanged)
    def videoSurface(self):
        return self.m_surface

    @videoSurface.setter
    def videoSurface(self, surface):  # 這裡正確地使用 setter 方法
        if self.m_surface == surface:
            return

        if self.m_surface and self.m_surface != surface and self.m_surface.isActive():
            self.m_surface.stop()

        self.m_surface = surface
        self.surfaceChanged.emit(self.m_surface)

        # m_backend->start();
        if self.m_surface and self.m_format.isValid():
            self.m_format = self.m_surface.nearestFormat(self.m_format)
            self.m_surface.start(self.m_format)
    
    def setFormat(self, width, height, frame_format):
        size = QSize(width, height)
        format = QVideoSurfaceFormat(size, frame_format)
        self.m_format = format

        if self.m_surface:
            if self.m_surface.isActive():
                self.m_surface.stop()
            self.m_format = self.m_surface.nearestFormat(self.m_format)
            if self.m_format.isValid():
                self.m_surface.start(self.m_format)

    @pyqtSlot(np.ndarray)
    def onVideoFrameReady(self, image):
        # Convert the numpy image to QImage
        if not self.m_surface or image is None:
            return

        if not image.flags['C_CONTIGUOUS']:
            continuous_frame = np.copy(image)
        else:
            continuous_frame = image

        height, width, channels = continuous_frame.shape

        if not self.m_isFormatSet:
            self.setFormat(width, height, QVideoFrame.Format_RGB32)
            self.m_isFormatSet = True

        # Qt expects 8-bits per channel RGB image, but numpy uses RGB, so we use Format_RGB888
        bytes_per_line = 3 * width
        self.m_image = QImage(
            continuous_frame.data,
            width, height, bytes_per_line,
            QImage.Format_RGB888).convertToFormat(QImage.Format_RGB32)

        # [Python] m_surface.present():
        #   不會自動將 QImage 轉為 QVideoFrame
        #   因此需要先將 QImage 包裝為 QVideoFrame
        #   才能丟進 m_surface.present()
        video_frame = QVideoFrame(self.m_image)
        if self.m_surface.isActive():
            self.m_surface.present(video_frame)

    @pyqtSlot()
    def play(self):
        self.m_backend.startVideo()

    @pyqtSlot()
    def stop(self):
        self.m_backend.framefinished()
