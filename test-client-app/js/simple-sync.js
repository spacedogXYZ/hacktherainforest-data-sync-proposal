var simpleSync = (function() {

    var simpleSync = {},
        port = 1337,
        onConnect = null;

    simpleSync.listenUDP = function() {
        var socketId;

        var onReceive = function(packet) {
            if (packet.socketId !== socketId) {
                return;
            }
            data = String.fromCharCode.apply(null, new Uint8Array(packet.data));
            console.log("RECV: "+data);

            switch(data){
                case 'OHAI':
                    console.log('Connect from '+packet.remoteAddress);
                    simpleSync.onConnect(packet);
                    break;
                default:
                    console.log('idk..');
            }
        };
        chrome.sockets.udp.onReceive.addListener(onReceive);

        chrome.sockets.udp.create({}, function(socketInfo) {
          socketId = socketInfo.socketId;
          // Setup event handler and bind socket.
          chrome.sockets.udp.onReceive.addListener(onReceive);
          chrome.sockets.udp.bind(socketId,
            "0.0.0.0", port, function(result) {
                if (result < 0) {
                    console.log("Error binding socket:" + result);
                    return;
              }
              console.log("Socket bound to port "+port);
          });
        });
    };

    simpleSync.requestChanges = function() {
        console.log('TBD');
    };

    return simpleSync;
}());
