function start_chatting(roomName, room_code) {
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
        + room_code
        + '/'
    );
    
    chatSocket.onmessage = function (msg) {
        data = JSON.parse(msg.data);
        console.log(data);
    };
}