from flask import Flask
from flask_socketio import SocketIO
import pymongo

from .channel import channel

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
socketio = SocketIO(app, message_queue='amqp://guest:guest@192.168.1.51:32770/')
mongodb = pymongo.MongoClient("mongodb://192.168.1.51:32768")
reputationdb = mongodb["reputation"]


def create_app(debug=False):
    """Create an application."""

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # socketio = socketio.init_app(app)
    # from app.handler import handler
    # socketio.start_background_task(target=handler)
    return app

