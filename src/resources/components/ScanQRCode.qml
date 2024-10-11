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
            spacing: (parent.width - playButton.width *4) / 5
            anchors.horizontalCenter: parent.horizontalCenter

            Rectangle {
                id: statusRect
                width: 30
                height: 30
                anchors.verticalCenter: playButton.verticalCenter

                Image {
                    id: statusImage
                    source: "qrc:resources/images/light_r.png"
                    asynchronous:true
                    fillMode: Image.PreserveAspectFit
                    anchors.fill: parent
                }
            }

            Label {
                id: statusLabel
                text: "Not Connected to DB"    

                anchors.verticalCenter: playButton.verticalCenter              
            }

            // row 1
            Button {
                id: playButton
                width: 120;
                height: 60;
                text: "Play"
                enabled: false

                onClicked: {
                    player.play();
                    playButton.enabled = false;
                    stopButton.enabled = true;
                }
            }

            Button {
                id: stopButton
                width: playButton.width;
                height: playButton.height;
                text: "Stop"
                enabled: false

                onClicked: {
                    player.stop();
                    playButton.enabled = true;
                }
            }
        }

        Row {
            id : areaRow
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

        Rectangle {
            id: checkInArea
            width: decodeArea.width
            height: 100
            border.color: "gray"
            border.width: 1
            color: "lightgray"
            anchors.right: areaRow.right

            Text {
                id: checkInStatus
                text: "尚未檢測到 QR Code"
                color: "orange"
                font.pointSize: 32
                anchors.centerIn: parent
                anchors.leftMargin: 10
            }
        }
    }

    Connections {
        target: manage

        function onDecodeMsgSig(isDetected, qr_data, isScanned) {
            if (isDetected) {
                decodeStatus.text = qr_data;
                if (isScanned) {
                    checkInStatus.text = "已報到過";
                    checkInStatus.color = "red";
                } else {
                    checkInStatus.text = "報到成功";
                    checkInStatus.color = "green";
                }
            }
        }
    }

    Component.onCompleted: {
        var db_name = "halloween";
        var collection_name = "Users";
        db.choose_collection(db_name, collection_name);
        playButton.enabled = true;
        statusLabel.text = "Already Connected to DB";
        statusImage.source = "qrc:resources/images/light_g.png";
    }
}


