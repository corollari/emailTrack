from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

sent={} #{imgID: clientID}
received={} #{clientID: [imgID1, imgID2]}
onlineClients={} #{clientID: socketID}

@app.route('/<string:imgID>.png')
def sendImage(imgID):
    if imgID in sent:
        if sent[imgID] in onlineClients:
            socketio.emit("received", imgID, room=onlineClients[sent[imgID]])
        else:
            received[sent[imgID]].append(imgID)
    return app.send_static_file('static/invisible.png')

@socketio.on('track')
def start_tracking(imgID):
    if "clientID" in session:
        sent[imgID]=session["clientID"]

@socketio.on('subscribe')
def subscribe(clientID):
    if "clientID" in session:
        return
    if clientID in onlineClients:
        return
    session["clientID"]=clientID
    onlineClients[clientID]=request.sid
    if clientID in received:
        for imgID in received[clientID]:
            emit("received", imgID)
    received[clientID]=[]

@socketio.on('disconnect')
def disconnect():
    del onlineClients[session["clientID"]]
