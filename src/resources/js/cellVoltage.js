WorkerScript.onMessage = function(msg) {
    var cell8 = { 'item': qsTr('Cell8(+)'), 'data': msg.cell8 + qsTr(' v')}
    var cell7 = { 'item': qsTr('Cell7'), 'data': msg.cell7 + qsTr(' v')}
    var cell6 = { 'item': qsTr('Cell6'), 'data': msg.cell6 + qsTr(' v')}
    var cell5 = { 'item': qsTr('Cell5'), 'data': msg.cell5 + qsTr(' v')}
    var cell4 = { 'item': qsTr('Cell4'), 'data': msg.cell4 + qsTr(' v')}
    var cell3 = { 'item': qsTr('Cell3'), 'data': msg.cell3 + qsTr(' v')}
    var cell2 = { 'item': qsTr('Cell2'), 'data': msg.cell2 + qsTr(' v')}
    var cell1 = { 'item': qsTr('Cell1(-)'), 'data': msg.cell1 + qsTr(' v')}
    var diff = { 'item': qsTr('V_diff_max'), 'data': msg.diff + qsTr(' mV')}

    msg.model.clear()
    msg.model.append(cell8);
    msg.model.append(cell7);
    msg.model.append(cell6);
    msg.model.append(cell5);
    msg.model.append(cell4);
    msg.model.append(cell3);
    msg.model.append(cell2);
    msg.model.append(cell1);
    msg.model.append(diff);

    msg.model.sync();
}
