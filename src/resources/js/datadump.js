WorkerScript.onMessage = function(msg) {
    //console.log(JSON.stringify(msg))
    if (Object.keys(msg).length === 1) {
        msg.model.clear();
        msg.model.sync();
    } else {
        var data = {'id': msg.id, 'name': msg.name, 'email': msg.email};
        
        msg.model.append(data);
        msg.model.sync();
    }
}
