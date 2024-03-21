import requests
import socket
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
grandparent_dir = os.path.dirname(parent_dir)


def read_config_file():
    with open(os.path.join(parent_dir, 'config.json')) as config_file:
        return json.load(config_file)


def check_user(user_number, ip):
    base_url = read_config_file()
    url = f'{base_url["master_system_url"]}/check_user/?user_id={user_number}&ip_address={ip}'
    r = requests.get(url)
    return r.json()


def check_machine_status(ip):
    base_url = read_config_file()

    url = f'{base_url["master_system_url"]}/vending_status/?ip_address={ip}'
    r = requests.get(url)
    return r.json()


def change_machine_status(ip):
    base_url = read_config_file()
    url = f'{base_url["master_system_url"]}/change_status/?ip_address={ip}'
    r = requests.get(url)
    return r.json()


def get_timeouts(ip):
    base_url = read_config_file()
    url = f'{base_url["master_system_url"]}/timeouts/?ip_address={ip}'
    r = requests.get(url)
    print(r.json())
    return r.json()


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address

    except socket.error as e:
        print(f"Error: {e}")
        return None


def checkout(user_id, product_id):
    base_url = read_config_file()
    url = f'{base_url["master_system_url"]}/checkout/?user_id={user_id}&product_id={product_id}'
    r = requests.get(url)
    return r.json()
