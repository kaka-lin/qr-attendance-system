import QtQuick 2.12
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
        currentIndex: 1

        TabButton {
            text: qsTr("EMAIL")
        }

        TabButton {
            text: qsTr("GOOGLE SHEET")
        }
    }

    SwipeView {
        id: view
        anchors.fill: parent
        currentIndex: bar.currentIndex

        EmailPage {
            id: emailPage
        }

        GoogleSheetPage {
            id: googleSheetPage
        }
    }
}
