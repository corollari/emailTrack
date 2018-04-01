# emailTimeServer
Flask server that tracks invisible pixels

Originally it was built with the intention of being used to handle the "message read" feature (aka "blue tick") of the emailTime app (which is also open-source and can be found here), which attaches tracking pixels to emails to monitor when messages are read, but you can use it for whatever you want.

Set up:
```bash
pip install requirements.txt
```

To run it:
```bash
FLASK_APP=server.py
flask run
```

## Guide
*Note:* All example code has been written in JavaScript but it shouldn't be hard to translate it to any other language that has a socket-io library available

Once the server is running, connect the client to the server through a socket-io connection:
```javascript
var socket = io();
```

After the connection has been established, identify your client by sending a `subscribe` event including the client's ID (unique string associated to your client which can be anything you wish) in the message:
```javascript
socket.emit("subscribe", "509f4b1");
```

Start tracking a new pixel by sending a `track` event along with a pixel id, a unique string that identifies the pixel to track (the pixel id string will be appended ".png" in order to form the filename of the tracking pixel):
```javascript
socket.emit("track", "r2d2");
```

When the pixel is requested (in this example, when a request is sent to `yourserver.com/r2d2.png`) a `received` event will be sent to the client, containing the id of pixel requested. In case the client is no longer online, the server will wait till the client comes back online and identifies itself sending a `subscribe` event, proceeding to send the `received` event after the identification.
