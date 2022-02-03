var socket = io();

// for debugging
socket.on('connect', function() {
    console.log('socket is open');
});
socket.on('disconnect', function() {
    console.log('socket is closed');
});

socket.on('json', function(data) {
    console.log('received message: ' + data.random_array)
});

function random(w, h) {
    socket.emit('random', w, h);
}
random(10, 10);
