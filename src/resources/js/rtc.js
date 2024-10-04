WorkerScript.onMessage = function(msg) {
    var data = {'time': msg.time, 'index': msg.index, 'soc': msg.soc};

    if (msg.model.count > 2) {
        msg.model.clear();
    }
    msg.model.append(data);
    msg.model.sync();
}
