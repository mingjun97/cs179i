import json
from time import sleep
from flask_socketio import emit


def handler():
    try:
        while 1:
            method_frame, header_frame, body = rabbitMQ.basic_get(queue='')
            if method_frame:
                print(method_frame, body)
                body = json.loads(body)
                with app.app_context():
                    emit('google', body['data'], namespace='/normal', broadcast=True)
                    socketio.sleep(0)
                continue
            sleep(0.3)
    except:
        return