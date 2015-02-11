var simpleSync;

function joinNetwork() {
    chrome.system.network.getNetworkInterfaces(function(interfaces) {
        var ipv4 = _.filter(interfaces, function(i) {
            return i.prefixLength == 24;
        });
        if (ipv4.length) {
            $('ul#interfaces input#local').val(ipv4[0].address);
        } else {
            $('ul#interfaces input#local').val('no network');
        }
    });

    simpleSync.onConnect = function(info) {
        $('ul#interfaces input#server').val(info.remoteAddress);
    };
    simpleSync.listenUDP(1337);
}

function randomString(length, chars) {
    var result = '';
    if (chars === undefined) { chars = 'abcdefghijklmnopqrstuvwxyz'; }
    for (var i = length; i > 0; --i) result += chars[Math.round(Math.random() * (chars.length - 1))];
    return result;
}

$('form #new').click(function(e) {
    e.preventDefault();

    var r = {'_id': new Date().toJSON(), 'content': randomString(10)};
    console.log(r);
    $('form textarea').append(r);

    //add to pouch
    window.db.put(r, 'id');
});

$(document).ready(function() {
    console.log('test-app start');
    joinNetwork();
});