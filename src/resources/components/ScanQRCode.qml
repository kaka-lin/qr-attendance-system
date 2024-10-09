import QtQuick 2.10
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.3
import QtMultimedia 5.15

import components.common 1.0

Rectangle {
    id: root
    anchors.fill: parent

    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 30

        spacing: 100

        GridLayout {
            id: grid

            rowSpacing: 12
            columnSpacing: 12

            // row 1
            Button {
                id: playButton
                text: "Play"

                Layout.row: 0
                Layout.column: 0

                onClicked: {
                    player.play();
                }
            }

            Button {
                id: stopButton
                text: "Stop"

                Layout.row: 0
                Layout.column: 1

                onClicked: {
                    player.stop();
                }
            }

            // row 2
            Rectangle {
                id: videoArea
                width: 600
                height: 300
                border.color: "gray"
                border.width: 1

                Layout.row: 1
                Layout.column: 0
                Layout.columnSpan: 2
    
                VideoOutput {
                    source: player
                    anchors.fill: parent
                    focus : visible // to receive focus and capture key events when visible
                }
            }
        }
    }
}


