import QtQuick 2.12
import QtQuick.Controls 1.4
// import QtQuick.Controls.Styles 1.4

Rectangle {
    id: root
    // color: parent.color  // 背景顏色
    anchors.fill: parent

    signal sendDataToGenQRCode(var data)

    property var normalG: Gradient {
        GradientStop { position: 0.0; color: "#fff" }
        GradientStop { position: 1.0; color: "#eee" }
    }

    property var pressG: Gradient {
        GradientStop { position: 0.0; color: "blue" }
        GradientStop { position: 1.0; color: "blue" }
    }

    ListModel { id: listModel }

    TableView {
        id: tableView
        
        backgroundVisible: false
        frameVisible: true
        sortIndicatorVisible: true

        anchors.fill: parent

        onRowCountChanged: {
            positionViewAtRow(rowCount - 1, ListView.End)
        }

        // TableView 背景 style
        rowDelegate: Rectangle {
            color: styleData.selected ? "lightblue" : "white"
        }

        // TableView 標題 style
        headerDelegate: Rectangle {
            implicitWidth: 10
            implicitHeight: 24
            gradient: styleData.pressed ? root.pressG : (styleData.containsMouse ? root.normalG: root.normalG)
            border.width: 1
            border.color: "gray"

            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 4
                anchors.right: parent.right
                anchors.rightMargin: 4
                text: styleData.value
                color: styleData.pressed ? "white" : "black"
                // font.bold: true
            }
        }

        TableViewColumn {
            id: dlcColumn
            title: "序號"
            role: "id"
            movable: false
            resizable: true
            width: tableView.viewport.width / 10

            delegate: Text {
                anchors.verticalCenter: parent.verticalCenter
                color: "black"
                elide: styleData.elideMode
                text: styleData.value
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }

        TableViewColumn {
            id: timeColumn
            title: "姓名"
            role: "name"
            movable: false
            resizable: true
            width: tableView.viewport.width / 3

            delegate: Text {
                anchors.verticalCenter: parent.verticalCenter
                color: "black"
                elide: styleData.elideMode
                text: styleData.value
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }

        TableViewColumn {
            id: canidColumn
            title: "EMAIL"
            role: "email"
            movable: false
            resizable: true
            width: tableView.viewport.width / 3

            delegate: Text {
                anchors.verticalCenter: parent.verticalCenter
                color: "black"
                elide: styleData.elideMode
                text: styleData.value
                verticalAlignment: Text.AlignVCenter
            }
        }

        model: listModel

        WorkerScript {
            id: dumpWorker
            source: "qrc:/resources/js/datadump.js" // 聲明js處理函數
        }            
    }

    Connections {
        target: manage

        // Sum signal handler
        function onDumpSig(id, name, email) {
            //console.log(id + ' ' + name + ' ' + emnil)
            var msg = {'id': id, 'name': name, 'email': email, 'model': listModel};
            dumpWorker.sendMessage(msg);
            sendDataToGenQRCode(msg);
        }

        function onDumpInit() {
            var msg = {'model': listModel}
            dumpWorker.sendMessage(msg);
        }
    }
}
