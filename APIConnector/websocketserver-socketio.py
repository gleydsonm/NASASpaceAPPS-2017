#!/usr/bin/env python
'''
API gateway for differents sources for SpaceAPPS System
Team Flash
Author: Gleydson Mazioli da Silva <gleydsonmazioli@gmail.com>

 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import socketio
import eventlet
import eventlet.wsgi
import json
import sys
import socket
from pymongo import MongoClient
from flask import Flask, render_template

MONGODB_SERVER='192.168.1.140'
#MONGODB_SERVER = '127.0.0.1'
MONGODB_DB = 'data'

thread = None
sio = socketio.Server(logger=True, async_mode='eventlet')
#sio = socketio.Server(async_mode='threading')
app = Flask(__name__)

mongo_client = MongoClient()
try:
    mongo_client = MongoClient(MONGODB_SERVER, 27017)
except Exception:
    sys.exit("Failure to connect to the mongo database")
mongo_db = mongo_client.MONGODB_DB

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my response10', {'data': 'Evento gerado pelo servidor'},
                 namespace='/')
#        sio.emit('getdata', {'data': 'Evento gerado pelo servidor'},
#                 namespace='/')

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    # Por padrao as paginas devem ser salvas dentro da pasta templates (flask)
    return render_template('index.html')

@sio.on('ping_from_client')
def ping(sid):
    sio.emit('pong_from_server', room=sid)

@sio.on('lixo')
def lixo(sid):
    sio.emit('myresponse40', {'data': 'Recebimento do evento lixo do client'},
             namespace='/')

@sio.on('my micro data', namespace='/')
def micro_data(sid, message):
    sio.emit('my response42', {'data': message['data']}, namespace='/')
    new_str = str(message['data']).replace("\'", "\"")
    new_dict = json.loads(new_str)
    print type(new_dict)
    print new_str
#    mongo_db.insert(new_dict)

#    print new_dict['ID']
#    print new_dict['data']

@sio.on('disconnect request', namespace='/')
def disconnect_request(sid):
    sio.disconnect(sid, namespace='/')

@sio.on('connect', namespace='/')
def test_connect(sid, environ):
    sio.emit('my response1', {'data': 'Conectado', 'count': 0}, room=sid,
             namespace='/')

@sio.on('disconnect', namespace='/')
def test_disconnect(sid):
    print('Cliente desconectado')

@sio.on('my event', namespace='/')
def test_message(sid, message):
    sio.emit('my response2', {'data': message['data']}, room=sid,
            namespace='/')

@sio.on('my broadcast event', namespace='/')
def test_broadcast_message(sid, message):
    sio.emit('my response3', {'data': message['data']}, namespace='/')


@sio.on('getdata', namespace='/')
def test_getdata_message(sid, message):
    sio.emit('getdata', {'data': message['data']}, namespace='/')

#
@sio.on('join', namespace='/')
def join(sid, message):
    sio.enter_room(sid, message['room'], namespace='/')
    sio.emit('my response4', {'data': 'Entrando na sala: ' + message['room']},
            room=sid, namespace='/')
#
@sio.on('leave', namespace='/')
def leave(sid, message):
    sio.leave_room(sid, message['room'], namespace='/')
    sio.emit('my response5', {'data': 'Deixando a sala: ' + message['room']},
            room=sid, namespace='/')
#
@sio.on('close room', namespace='/')
def close(sid, message):
    sio.emit('my response6',
            {'data': 'A sala ' + message['room'] + ' foi encerrada.'},
            room=message['room'], namespace='/')
    sio.close_room(message['room'], namespace='/')
#
@sio.on('my room event', namespace='/')
def send_room_message(sid, message):
    sio.emit('my response7', {'data': message['data']}, room=message['room'],
            namespace='/')



if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8775)), app)
