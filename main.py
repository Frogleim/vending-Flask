from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from api_connect import master_system
from datetime import datetime, timedelta

import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(seconds=15)


def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


@app.route('/')
def home():
    ip = get_ipv4_address()
    user_id = request.form.get('user_id')
    print(user_id)
    print(ip)
    try:
        machine_status = master_system.check_machine_status(ip=ip)
        print(machine_status)
        if 'success' in machine_status['status']:
            return render_template('index.html')
        else:
            return render_template('error.html')
    except Exception as e:
        print(e)
        return render_template('error.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    user_id = request.form.get('user_id')
    session['user_id'] = user_id

    # Check if user_id is in session, indicating an active session
    if 'user_id' in session:
        ip_address = master_system.get_ip_address()
        status = master_system.check_user(int(user_id), ip_address)
        data = {"master_system": status['data'], 'user_id': user_id}
        print(status['data'])
        if 'success' in status['status']:
            # Do something with user_id, e.g., save it to a database
            session['user_id'] = user_id
            return render_template('home.html', data=data, user_id=user_id)

    # If user_id is not in session or the check_user fails, redirect to the home page
    return redirect(url_for('home'))


@app.route('/takeout_goods', methods=['POST'])
def takeout_goods():
    try:
        snipe_id = request.form.get('snipe_id')
        user_id = request.form.get('user_id')
        print(snipe_id, user_id)
        master_system.checkout(user_id, snipe_id)
        response_data = {'message': 'Successfully processed the takeout request'}
        return render_template('takeout.html')
    except Exception as e:
        # Log any errors that occur
        print(f"Error processing takeout request: {str(e)}")
        return render_template('error.html')


if __name__ == '__main__':
    ip = get_ipv4_address()
    # Run the app on host 0.0.0.0 and port 5000
    app.run(host=f'{ip}', port=5000, debug=True)
