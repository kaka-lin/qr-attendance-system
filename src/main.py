import os
import sys
from PyQt5.QtCore import QCoreApplication, QUrl, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, QQmlContext

from src import qml, components
from src.app.my_media_player import MyMediaPlayer
from src.threads.manage_threads import ManageThreads
from src.app.mongo_controller import MongoController


def run(app, pwd, mode):
    # Create QML engine
    engine = QQmlApplicationEngine()
    context = engine.rootContext()

    # mongoDB
    uri = os.environ["MONGO_URI"]
    mongo_controller = MongoController(uri)
    mongo_controller.connect()
    # manage threads
    manage = ManageThreads(mongo_controller)
    # manage is backend of MyMediaPlayer for choose video source
    player = MyMediaPlayer(manage)

    context.setContextProperty("manage", manage)
    context.setContextProperty("player", player)
    context.setContextProperty("db", mongo_controller)

    if mode == "prod":
        engine.addImportPath('qrc:///resources')
        engine.load(QUrl('qrc:/resources/main.qml'))
    else:
        engine.addImportPath(os.path.join(pwd, "src/resources"))
        engine.load(QUrl(os.path.join(pwd, "src/resources/main.qml")))

    # Connect the app's quit signal to MongoController's close method
    app.aboutToQuit.connect(mongo_controller.close)

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
