import serial
import time
import logging
import socketio

# Connect to the Flask app's SocketIO server
sio = socketio.Client()

class RFIDReader:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
        self.logger = logging.getLogger(__name__)

    def read_rfid(self):
        try:
            data = self.serial.readline().decode().strip()
            return data
        except Exception as e:
            self.logger.error(f"Error reading RFID: {e}")
            return None

    def close(self):
        self.serial.close()

# Initialize the RFID reader
reader = RFIDReader()

# Connect to the SocketIO server
@sio.event
def connect():
    print('Connected to SocketIO server')

# Start reading RFID data and emit it to the Flask app
def read_and_emit_rfid():
    while True:
        rfid_data = reader.read_rfid()
        if rfid_data:
            # Emit RFID data to the Flask app
            sio.emit('rfid_data', rfid_data)
            time.sleep(1)

# Start the RFID reading and emitting process
if __name__ == '__main__':
    sio.connect('http://your_flask_app_server:5000')  # Replace with your Flask app server URL
    sio.start_background_task(read_and_emit_rfid)
    sio.wait()
    reader.close()
