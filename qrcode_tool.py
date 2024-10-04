#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import platform

from PyQt5.QtGui import QGuiApplication
from src import main


if __name__ == "__main__":
    mode = ''
    # use: python3 qrcode_tool.py prod
    if len(sys.argv) == 2:
        mode = sys.argv[1]

    if hasattr(sys, "frozen"):
        # running in a bundle
        pwd = os.path.dirname(os.path.abspath(sys.executable))
        mode = 'prod'
    else:
        # running live
        pwd = os.path.dirname(os.path.abspath(__file__))

    # OS
    if platform.system() == 'Linux':
        os.environ['QT_QPA_FONTDIR'] = '/usr/share/fonts/truetype/dejavu/'
        os.environ['LD_LIBRARY_PATH'] = '/usr/local/qt5/lib/'
        os.environ['PATH'] = '/usr/local/qt5/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games'
    elif platform.system() == 'Windows':
        pwd = ''

    # start app
    app = QGuiApplication(sys.argv)
    main.run(app, pwd, mode)
