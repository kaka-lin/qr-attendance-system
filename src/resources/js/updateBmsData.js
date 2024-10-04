WorkerScript.onMessage = function(msg) {
    var data1 = { 'item': qsTr('Firmware Version'), 'data': msg.version };
    var data2 = { 'item': qsTr('Pack Voltage'), 'data': msg.voltage + qsTr(' v') };
    var data3 = { 'item': qsTr('Pack Current'), 'data': msg.current + qsTr(' mA') };
    var data4 = { 'item': qsTr('Max Cell Temp'), 'data': msg.temp+ qsTr(' °') };

    msg.model.clear()
    msg.model.append(data1);
    msg.model.append(data2);
    msg.model.append(data3);
    msg.model.append(data4);

    msg.model.sync();
}
