import os
import sys
from PyQt5.QtCore import QCoreApplication, QUrl, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, QQmlContext

from src.app.my_media_player import MyMediaPlayer
from src.threads.manage_threads import ManageThreads
from src import qml, components


def run(app, pwd, mode):
    # Create QML engine
    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    # mange thread and MyMediaPlayer
    manage = ManageThreads()
    player = MyMediaPlayer(manage)
    context.setContextProperty("manage", manage)
    context.setContextProperty("player", player)

    if mode == "prod":
        engine.addImportPath('qrc:///resources')
        engine.load(QUrl('qrc:/resources/main.qml'))
    else:
        engine.addImportPath(os.path.join(pwd, "src/resources"))
        engine.load(QUrl(os.path.join(pwd, "src/resources/main.qml")))

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
