'use strict';

const io = require('socket.io-client');

const socket = io.connect('http://localhost:3005');

let fakeData = () => {
  console.log('Hello World');
  
  let num = Math.random();

  socket.emit('moisture-data', num);
};

fakeData();
