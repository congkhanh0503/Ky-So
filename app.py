from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os
import base64
import uuid
import json
import time
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
KEY_STORAGE = 'keys'  # Chỉ lưu khóa công khai
HISTORY_FILE = 'history.json'
if not os.path.exists(KEY_STORAGE):
    os.makedirs(KEY_STORAGE)

# Dictionary to store connected clients
clients = {}

# Load or initialize history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def clean_old_keys():
    now = time.time()
    expiration = 24 * 60 * 60  # 24 hours in seconds
    history = load_history()
    updated_history = []
    for entry in history:
        if now - entry['timestamp'] < expiration:
            updated_history.append(entry)
        else:
            key_path = os.path.join(KEY_STORAGE, f"{entry['key_id']}.pem")
            if os.path.exists(key_path):
                os.remove(key_path)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(updated_history, f, indent=2)

@socketio.on('connect')
def handle_connect():
    clients[request.sid] = {'role': None}
    emit('connection_status', {'message': 'Kết nối WebSocket thành công!'})

@socketio.on('set_role')
def handle_set_role(data):
    role = data.get('role')
    clients[request.sid] = {'role': role}
    emit('connection_status', {'message': f'Đã đăng ký vai trò: {role}'})

@socketio.on('send_file')
def handle_send_file(data):
    filename = data['filename']
    file_content = data['file_content']  # Base64 encoded
    private_key_pem = data['private_key']
    public_key_pem = data['public_key']
    
    try:
        # Decode file content
        decoded_content = base64.b64decode(file_content)
        
        # Create SHA256 hash
        hash_obj = SHA256.new(decoded_content)

        # Sign with private key
        private_key = RSA.import_key(private_key_pem)
        signature = pkcs1_15.new(private_key).sign(hash_obj)
        signature_b64 = base64.b64encode(signature).decode('utf-8')

        # Generate unique key_id
        key_id = str(uuid.uuid4())
        
        # Store public key
        key_path = os.path.join(KEY_STORAGE, f"{key_id}.pem")
        with open(key_path, 'w') as f:
            f.write(public_key_pem)

        # Save to history
        entry = {
            'filename': filename,
            'signature': signature_b64,
            'key_id': key_id,
            'timestamp': time.time(),
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_history(entry)

        # Send to all receivers
        for sid, client in clients.items():
            if client['role'] == 'receiver':
                emit('receive_file', {
                    'filename': filename,
                    'file_content': file_content,
                    'signature': signature_b64,
                    'public_key': public_key_pem
                }, to=sid)
    except Exception as e:
        emit('error', {'message': f'Lỗi khi xử lý file: {str(e)}'}, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sender')
def sender():
    return render_template('sender.html')

@app.route('/receiver')
def receiver():
    return render_template('receiver.html')

@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    try:
        key = RSA.generate(2048)
        private_key = key.export_key().decode('utf-8')
        public_key = key.publickey().export_key().decode('utf-8')
        return jsonify({'private_key': private_key, 'public_key': public_key})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify_signature', methods=['POST'])
def verify_signature():
    file = request.files.get('file')
    signature_b64 = request.form.get('signature')
    public_key_pem = request.form.get('public_key')
    if not file or not signature_b64 or not public_key_pem:
        return jsonify({'error': 'Missing file, signature, or public key'}), 400

    try:
        # Read file content
        data = file.read()

        # Create SHA256 hash
        hash_obj = SHA256.new(data)

        # Verify signature
        public_key = RSA.import_key(public_key_pem)
        signature = base64.b64decode(signature_b64)
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        return jsonify({'valid': True})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 400

@app.route('/history', methods=['GET'])
def get_history():
    clean_old_keys()
    return jsonify(load_history())

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')