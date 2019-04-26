from routes import init_api_routes, init_website_routes
from Data_Ingestor.twitter_streaming_producer import startStreaming

import sys

sys.path.append("../")  # go to parent dir


# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit, send
from flask import Flask, render_template, url_for, copy_current_request_context
from threading import Thread, Event

# Imports for Web Sockets
from threading import Lock
from Data_Ingestor.streaming import DataFlow
from Data_Ingestor.streaming import *



async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

init_api_routes(app)
init_website_routes(app)

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()
flow = None


def background_thread():
    print("background thread")
    global flow
    print("Stream is flowing...")
    flow = DataFlow.factory('historical')
    flow.start(socketio)



@socketio.on('stop_stream', namespace='/test')
def stop_stream():
    print("stop_stream")
    global thread
    print("Stream flow is ending...")
    thread = None
    flow.stop()


@socketio.on('start_stream', namespace='/test')
def start_stream():
    print("start_stream")
    global thread
    with thread_lock:
        if thread is None:
            print("Starting thread...")
            thread = socketio.start_background_task(background_thread)


if __name__ == "__main__":
    print("Running server...")
    start_stream()
    socketio.run(app, debug=1)


