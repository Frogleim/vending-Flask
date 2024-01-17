from flask import Flask, render_template, request
from api_connect import master_system
import socket

app = Flask(__name__)


def get_ipv4_address():
    try:
        host_name = socket.gethostname()
        print(host_name)
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None


@app.route('/')
def home():
    ip = get_ipv4_address()
    machine_status = master_system.check_machine_status(ip=ip)
    if 'success' in machine_status['status']:
        return render_template('index.html')
    else:
        return render_template('error.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    user_id = request.form.get('user_id')
    ip_address = master_system.get_ip_address()
    status = master_system.check_user(int(user_id), ip_address)
    if 'success' in status['status']:
        # Do something with user_id, e.g., save it to a database
        return render_template('home.html', data=status['data'])
    else:
        return render_template('error.html')


if __name__ == '__main__':
    # Run the app on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
