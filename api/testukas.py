import time
from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    
    return {'time': time.time()}

@app.route('/send', methods=['POST'])
def get_data():
    print('Recieved from client: {}'.format(request.data))
    return Response('We recieved something…')