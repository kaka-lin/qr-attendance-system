import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "pages"

Page {
    id: root
    width: parent.width
    height: parent.height

    header: TabBar {
        id: bar
        width: parent.width
        currentIndex: view.currentIndex

        TabButton {
            text: qsTr("QR Code generator")
        }
    }

    SwipeView {
        id: view
        anchors.fill: parent
        currentIndex: bar.currentIndex

        QRCodePage {
            id: qrcodePage
        }
    }
}
