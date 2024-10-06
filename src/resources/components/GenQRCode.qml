import QtQuick 2.12
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.2

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
            Label {
                text: "Email:"

                Layout.row: 0
                Layout.column: 0
            }

            TextField {
                id: emailFileText
                placeholderText: qsTr("Email")
                Layout.preferredWidth: 300

                Layout.row: 0
                Layout.column: 1

                onAccepted: {
                    generateButton.enabled = true;
                }

                onTextChanged: {
                    generateButton.enabled = false;
                }
            }

            Rectangle {
                width: 200
                height: 200
                border.color: "gray"
                border.width: 1

                Layout.row: 0
                Layout.column: 2
    
                Image {
                    id: qrcodeImage
                    source: ""
                    asynchronous:true
                    fillMode: Image.PreserveAspectFit
                    anchors.fill: parent
                    anchors.margins: 5
                }
            }

            // row 2
            Button {
                id: generateButton
                text: "Generate"
                enabled: false

                Layout.row: 1
                Layout.column: 1

                onClicked: {
                    var data = emailFileText.text;

                    manage.qrcode_generate(data, "", "");
                }
            }
        }
    }

    Connections {
        target: manage

        function onQrcodeGenMsg(genMsg) {
            var image_path = genMsg;
            qrcodeImage.source = image_path;
        }
    }
}
