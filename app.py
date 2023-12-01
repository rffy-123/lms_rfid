from flask import Flask, g, session, redirect, render_template, request, jsonify, Response
from Misc.functions import *
from flask_socketio import SocketIO, emit
from Models.DAO import DAO
from Models.UserDAO import UserDAO

app = Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'
socketio = SocketIO(app)

@socketio.on('rfid_data')
def handle_rfid_data(data):
    # Handle RFID data received from the client
    print(f"Received RFID data: {data}")
    user_dao = UserDAO(DAO)
    # Query the database to find the user associated with the RFID data
    user = user_dao.getByRFID(data)
    if user:
        # Set the user in the Flask global context (g) for later access
        g.user = user

        # Emit the RFID data to all connected clients
        emit('rfid_data', data)
    else:
        print("User not found for the provided RFID data.")

if __name__ == '__main__':
    socketio.run(app)

# Setting DAO Class
from Models.DAO import DAO

DAO = DAO(app)

# Registering blueprints
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)