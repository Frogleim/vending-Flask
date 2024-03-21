import time
import ast
import subprocess
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from api_connect import master_system, logs_setting
from datetime import datetime, timedelta, timezone
import requests
import socket
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)


def read_config_file():
    with open(os.path.join(parent_dir, 'config.json')) as config_file:
        return json.load(config_file)


def read_config():
    with open('api_connect/controller_settings.json', 'r') as conf:
        data = json.load(conf)
    return data


def send_command(cell_number):
    data = read_config_file()
    shelf_number = None
    spiral_number = None
    cells_data = read_config()
    for items in cells_data['cells']:
        print(items)
        if items['cell'] == int(cell_number):
            shelf_number = items['ndeck']
            spiral_number = items['spiral']
    dat = {
        "shelf_number": shelf_number,
        "spiral_number": spiral_number
    }
    print(data)
    r = requests.post(f'{data["controller_api_url"]}/get_goods/', json=dat)
    if r.status_code == 200:
        return True
    else:
        return False


def get_timeouts():
    ip = get_ipv4_address()
    timeouts = master_system.get_timeouts(ip)
    return timeouts



def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


@app.route('/reset_session_timeout')
def reset_session_timeout():
    if 'last_activity' in session:
        # Update the last activity timestamp to the current time
        session['last_activity'] = time.time()
        print('Pop up reseted')
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Session does not exist or last activity not set'}), 400

#67123663928
@app.route('/check_session_status')
def check_session_status():

    ex_time = get_timeouts()['users_timeout']
    if 'user_id' in session and 'last_activity' in session:
        last_activity_time = session['last_activity']
        logs_setting.actions_logger.info(f'Last activity: {last_activity_time}')
        current_time = time.time()
        logs_setting.actions_logger.info(f'Current time: {current_time}')
        print(current_time - last_activity_time)
        print(f'Master expiration time: {ex_time}, type: {type(ex_time)}')

        midpoint = ex_time / 2

        if current_time - last_activity_time > float(ex_time):
            session.pop('user_id', None)
            print(f'Session expired: {current_time - last_activity_time}')
            return jsonify({'status': 'expired'})
        elif current_time - last_activity_time >= midpoint:
            return jsonify({'status': 'half_expired'})

    return jsonify({'status': 'active'})


@app.route('/check_session_status_operator')
def check_session_status_operator():
    expire_time = get_timeouts()['users_timeout']
    logs_setting.actions_logger.info(f'Expire time: {expire_time}')
    if 'user_id' in session and 'last_activity' in session:
        last_activity_time = session['last_activity']
        expiration_time = last_activity_time + expire_time
        current_time = time.time()
        logs_setting.actions_logger.info(f'Current time: {current_time}')
        # Calculate the midpoint between last activity time and expiration time
        midpoint = last_activity_time + (expire_time / 2)

        if current_time > expiration_time:
            session.pop('user_id', None)
            return jsonify({'status': 'expired'})
        elif current_time > midpoint:
            return jsonify({'status': 'half_expired'})

    return jsonify({'status': 'active'})


@app.route('/')
def home():
    ip = get_ipv4_address()
    user_id = request.args.get('user_id')
    try:
        machine_status = master_system.check_machine_status(ip=ip)
        if 'success' in machine_status['status']:
            print(session)
            session['user_id'] = user_id
            logs_setting.actions_logger.info(f'New session: {session["last_activity"]}')
            return render_template('index.html')
        else:
            session['user_id'] = user_id
            logs_setting.actions_logger.info(f'New session: {session["last_activity"]}')

            return render_template('serivce.html')
    except Exception as e:
        logs_setting.error_logs_logger.error(e)
        return render_template('serivce.html')


@app.route('/service')
def service():
    return render_template('serivce.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    user_id = request.form.get('user_id') or session.get('user_id')
    if 'user_id' in session:
        ip_address = master_system.get_ip_address()
        session['last_activity'] = time.time()

        try:
            status = master_system.check_user(int(user_id), ip_address)
            print(status)
            data_dict = {"master_system": status['data'], 'user_id': user_id}
            print(data_dict)
            if 'success' in status['status']:
                session['user_id'] = user_id
                return render_template('home.html', data=data_dict, user_id=user_id, fio=status['user_data'])
            if status['status'] == 'operator':
                session['user_id'] = user_id
                return render_template('service_status.html')
        except Exception as e:

            logs_setting.error_logs_logger.error(f"Exception: {str(e)}")
            return render_template('login_error.html')
    return redirect(url_for('home'))


@app.route('/proccessing', methods=['POST'])
def proccessing():
    snipe_id = request.form.get('snipe_id')
    user_id = request.form.get('user_id')
    print(user_id)
    image_url = request.form.get('image')
    fio = request.form.get('fio')  # Get the value of 'fio' from the form
    product_name = request.form.get('goods')  # Get the value of 'goods' from the form
    cell_number = request.form.get('cell_number')  # Get the value of 'cell_number' from the form
    success_data = {'image_url': image_url, 'fio': fio, 'product_name': product_name, "snipe_id": snipe_id,
                    'cell_number': cell_number, 'user_id': user_id}
    return render_template('wait.html', data=success_data)


@app.route('/takeout', methods=['POST'])
def takeout_goods():
    try:
        snipe_id = request.form.get('snipe_id')
        print(snipe_id)
        user_id = request.form.get('user_id')
        print(f'User ID {user_id}')
        image_url = request.form.get('image')
        fio = request.form.get('fio')  # Get the value of 'fio' from the form
        product_name = request.form.get('goods')  # Get the value of 'goods' from the form
        cell_number = request.form.get('cell_number')  # Get the value of 'cell_number' from the form
        print(cell_number)
        # status = True
        try:
            status = send_command(cell_number=cell_number)
            if status:
                print(type(fio))
                print(product_name)
                master_system.checkout(user_id, snipe_id)
                logs_setting.actions_logger.info(
                    f"Processing takeout request for snipe_id: {snipe_id}, user_id: {user_id}")
                logs_setting.actions_logger.info(f"User: {user_id}, product id: {snipe_id}")
                success_data = {'image_url': image_url, 'fio': fio, 'product_name': product_name}
                success(success_data)
                return render_template('success.html', data=success_data)
            else:
                return render_template('takeout_error.html')  # Return the rendered template
        except Exception as e:
            print(e)
            return render_template('takeout_error.html')  # Return the rendered template
    except Exception as e:
        logs_setting.error_logs_logger.error(f"Error processing takeout request: {str(e)}")
        return render_template('takeout_error.html')  # Return the rendered template


@app.route('/success')
def success(data):
    return render_template('success.html', data=data)


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
        logs_setting.error_logs_logger.error(f"Error changing machine status: {str(e)}")
        return jsonify({'status': 'failed', 'message': str(e)})

def open_browser(ip_address):
    try:
        subprocess.run(['./firefox_setup.sh', ip_address], check=True)
        return 'Browser opened successfully'
    except subprocess.CalledProcessError as e:
        return False


if __name__ == '__main__':
    ip = get_ipv4_address()
    print(ip)
    
    # Open browser using threading
    import threading
    browser_thread = threading.Thread(target=open_browser, args=(ip,))
    browser_thread.start()

    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host=ip, port=5000, debug=True)
