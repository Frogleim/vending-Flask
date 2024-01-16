from flask import Flask, render_template, request
from api_connect import master_system

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


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
    app.run(debug=True)
