import QtQuick 2.8
import QtQuick.Controls 2.1

import components 1.0

Rectangle {
    id: root
    property string current_module: ""

    GenQRCode {
        current_module: root.current_module
    }
}
