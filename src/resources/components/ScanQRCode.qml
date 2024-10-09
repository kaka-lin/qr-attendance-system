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
        anchors.fill: parent
        anchors.topMargin: 15

        spacing: 30

        Row {
            id: btnRow
            spacing: (parent.width - playButton.width *2) / 4
            anchors.horizontalCenter: parent.horizontalCenter

            // row 1
            Button {
                id: playButton
                width: 120;
                height: 60;
                text: "Play"
                onClicked: {
                    player.play();
                }
            }

            Button {
                id: stopButton
                width: playButton.width;
                height: playButton.height;
                text: "Stop"
                onClicked: {
                    player.stop();
                }
            }
        }

        Row {
            id : areaColumn
            spacing: 30
            anchors.horizontalCenter: parent.horizontalCenter

            Rectangle {
                id: videoArea
                width: (root.width - 90) / 2
                height: 300
                border.color: "gray"
                border.width: 1
                VideoOutput {
                    source: player
                    anchors.fill: parent
                    focus : visible // to receive focus and capture key events when visible
                }
            }

            Rectangle {
                id: decodeArea
                width: videoArea.width
                height: 300
                border.color: "gray"
                border.width: 1
                color: "black"

                Text {
                    id: decodeStatus
                    color: "white"
                    text: ""

                    anchors.centerIn: parent
                    anchors.leftMargin: 10
                }
            }
        }
    }

    Connections {
        target: manage

        function onDecodeMsgSig(qr_data) {
            decodeStatus.text = qr_data;
        }
    }
}


