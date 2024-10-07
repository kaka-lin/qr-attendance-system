import QtQuick 2.12
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Universal 2.0
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2

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
            text: qsTr("SCAN")
        }
    }

    SwipeView {
        id: view
        anchors.fill: parent
        currentIndex: bar.currentIndex

        ScanPage {
            id: scanPage
        }
    }
}
