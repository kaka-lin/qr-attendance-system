import QtQuick 2.12
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.2
// import QtQuick.Controls 1.4 // TableViewColumn
import QtQuick.Dialogs 1.2

import components 1.0
import components.common 1.0

Rectangle {
    id: root
    anchors.fill: parent

    property string qr_data: ""
    property string output_file: ""

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
                text: "Google Sheet Key:"

                Layout.row: 0
                Layout.column: 0
            }

            TextField {
                id: gsKeyFileText
                placeholderText: qsTr("Credentials.json")
                Layout.preferredWidth: 300

                Layout.row: 0
                Layout.column: 1
            }

            Button {
                text: "Open"

                Layout.row: 0
                Layout.column: 2

                onClicked: {
                    gsKeyFileDialog.open();
                }
            }

            // row 2
            Label {
                text: "Google Sheet URL:"

                Layout.row: 1
                Layout.column: 0
            }

            TextField {
                id: gsURLText
                placeholderText: qsTr("https://docs.google.com/spreadsheets/d/試算表ID/edit")
                Layout.preferredWidth: 500

                Layout.row: 1
                Layout.column: 1
                Layout.columnSpan: 2
            }

            // row 2
            Rectangle {
                width: 600
                height: 300

                Layout.row: 2
                Layout.column: 0
                Layout.columnSpan: 2

                GoogleSheetDump {
                    id: googleSheetDumpArea
                }
            }  
            
            Column {
                id: row
                spacing: 10

                Layout.row: 2
                Layout.column: 2

                Button {
                    id: genQRCodeSheetButton
                    text: "generate_code_sheet"
                    enabled: gsKeyFileText.text !== "" && gsURLText.text !== "" ? true : false

                    onClicked: {
                        var service_file = gsKeyFileText.text;
                        var sheet_url = gsURLText.text;
                        manage.genQRCodeSheet(service_file, sheet_url);
                    }
                }
            }
        }
    }

    FileDialog {
        id: gsKeyFileDialog
        title: "Please choose a file"
        // raspberry pi device path
        folder: Qt.platform.os === "linux" ? "/media/pi" : shortcuts.home

        onAccepted: {
           var filepath = new String(fileUrl);
           if (Qt.platform.os == "windows") {
               gsKeyFileText.text = filepath.slice(8);
           } else {
               gsKeyFileText.text = filepath.slice(7);
           }
        }
    }
}
