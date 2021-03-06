from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from uuid import uuid4
import json
import requests
import os

# global variables
MIN_SIM = 0.7
MAX_SIM = 0.97

# env variables
port = os.environ.get("API_PORT")
api_key = os.environ.get("API_KEY")

# configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = '971cf9854ab52d7c643b13c74795f86b5bc09ab6554e42c27155c581bdf937d5'
socket_ = SocketIO(app)

# load QA pairs
f = open('dataset/qa_data.json', encoding='utf-8')
qa_data = json.load(f)
f.close()


# serve index page
@app.route('/')
def index():
    print('REFRESHING')
    return render_template('index.html', async_mode=socket_.async_mode)


# on connect, set user token as randomly generated ID
@socket_.on('connect', namespace='/chat')
def connect():
    user_token = uuid4()
    session["user_token"] = user_token
    print(f'[{session["user_token"]}]: connected')


# on start
@socket_.on('start', namespace='/chat')
def chat_start():
    # send welcome message
    emit('bot_response', {
        'data': "Hello, welcome to the chatbot!<br><br>I can answer your questions, what would you like to know about?"})


# on client send message
@socket_.on('send_message', namespace='/chat')
def chat_send_message(message):
    # similarity API URL
    domain = 'host.docker.internal'
    sim_api = f'http://{domain}:{port}/similarity'

    # default error message
    max_sim = MIN_SIM
    best_ans = "Sorry, we are not able to answer your question."

    # find answer
    for qa_pair in qa_data:
        try:
            # POST request to similarity API
            r = requests.post(
                sim_api, json={'api_key': api_key, 's1': message['data'], 's2': qa_pair[0]})
        except Exception:
            # if unable to connect, send suitable error message
            print(Exception)
            emit('bot_response', {
                'data': "Sorry, this service is currently unavailable."})
            return None

        # if status OK
        if (r.status_code == 200):
            # if similarity above current max, set as best answer so far
            if (r.json()['sim'] > max_sim):
                max_sim = r.json()['sim']
                best_ans = qa_pair[1].capitalize()

        if (max_sim >= MAX_SIM):
            # if better than expected max similarity threshold
            break

    print(f'[{session["user_token"]}]: {best_ans}, {max_sim}')

    # emit best answer back to client
    emit('bot_response', {'data': best_ans})


# on disconnect request
@socket_.on('disconnect_request', namespace='/chat')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    # emit greeting message with disconnect callback
    emit('bot_response', {
         'data': 'Thank you for using our service!'}, callback=can_disconnect)


if __name__ == '__main__':
    socket_.run(app, debug=True)
