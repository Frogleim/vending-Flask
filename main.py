import time

from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from api_connect import master_system
from datetime import datetime, timedelta, timezone

import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_timeouts():
    ip = get_ipv4_address()
    timeouts = master_system.get_timeouts(ip)
    return timeouts


normal_user_timeout = timedelta(seconds=15)
operator_timeout = timedelta(seconds=10)


def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


@app.route('/check_session_status')
def check_session_status():
    expire_time = timedelta(seconds=get_timeouts()['users_timeout'])
    print(expire_time)
    if 'user_id' in session and 'last_activity' in session:
        last_activity_time = session['last_activity']
        expiration_time = last_activity_time + expire_time
        current_time = datetime.now(timezone.utc)
        print(current_time > expiration_time)
        if current_time > expiration_time:
            session.pop('user_id', None)
            return jsonify({'status': 'expired'})

    return jsonify({'status': 'active'})


@app.route('/check_session_status_operator')
def check_session_status_operator():
    expire_time = timedelta(seconds=get_timeouts()['operator_timeout'])
    if 'user_id' in session and 'last_activity' in session:
        last_activity_time = session['last_activity']
        expiration_time = last_activity_time + expire_time
        current_time = datetime.now(timezone.utc)
        print(current_time > expiration_time)
        if current_time > expiration_time:
            session.pop('user_id', None)
            return jsonify({'status': 'expired'})

    return jsonify({'status': 'active'})


@app.route('/')
def home():
    ip = get_ipv4_address()
    user_id = request.args.get('user_id')
    print(user_id)
    print(ip)
    try:
        machine_status = master_system.check_machine_status(ip=ip)
        print(machine_status)
        if 'success' in machine_status['status']:
            print(session)
            session['user_id'] = user_id
            session['last_activity'] = datetime.now(timezone.utc)
            return render_template('index.html')
        else:
            session['user_id'] = user_id
            session['last_activity'] = datetime.now(timezone.utc)
            return render_template('serivce.html')
    except Exception as e:
        print(e)
        return render_template('serivce.html')


@app.route('/service')
def service():
    return render_template('serivce.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    user_id = request.form.get('user_id') or session.get('user_id')
    print('User id', user_id)
    if 'user_id' in session:
        print(f'Session: {session}')
        ip_address = master_system.get_ip_address()
        try:
            status = master_system.check_user(int(user_id), ip_address)
            print(status)
            data = {"master_system": status['data'], 'user_id': user_id}
            if 'success' in status['status']:
                session['user_id'] = user_id
                return render_template('home.html', data=data, user_id=user_id, fio=status['user_data'])
            if status['status'] == 'operator':
                # Do something with user_id, e.g., save it to a database
                session['user_id'] = user_id
                return render_template('service_status.html')
        except Exception as e:
            print(f"Exception: {str(e)}")
            return render_template('login_error.html')
    return redirect(url_for('home'))


@app.route('/takeout', methods=['POST'])
def takeout_goods():
    try:
        snipe_id = request.form.get('snipe_id')
        user_id = request.form.get('user_id')
        print(user_id)
        master_system.checkout(user_id, snipe_id)
        print(f"Processing takeout request for snipe_id: {snipe_id}, user_id: {user_id}")
        response_data = {'message': 'Successfully processed the takeout request'}
        return jsonify(response_data)
    except Exception as e:
        print(f"Error processing takeout request: {str(e)}")
        return jsonify({'error': str(e)})


@app.route('/success')
def success():
    return render_template('success.html')


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_message='Internal Server Error'), 500


@app.route('/change_machine_status', methods=['GET'])
def change_machine_status():
    try:
        ip = get_ipv4_address()
        result = master_system.change_machine_status(ip)
        if result['status'] == 'success':
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failed', 'message': result.get('message', 'Unknown error')})
    except Exception as e:
        print(f"Error changing machine status: {str(e)}")
        return jsonify({'status': 'failed', 'message': str(e)})


if __name__ == '__main__':
    ip = get_ipv4_address()
    # Run the app on host 0.0.0.0 and port 5000
    app.run(host=f'{ip}', port=5000, debug=True)
