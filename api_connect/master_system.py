import requests
import socket


def check_user(user_number, ip):
    url = f'http://192.168.9.96:8000/check_user/?user_id={user_number}&ip_address={ip}'
    r = requests.get(url)
    return r.json()


def check_machine_status(ip):
    url = f'http://192.168.9.96:8000/vending_status/?ip_address={ip}'
    r = requests.get(url)
    return r.json()


def change_machine_status(ip):
    url = f'http://192.168.9.96:8000/change_status/?ip_address={ip}'
    r = requests.get(url)
    return r.json()


def get_timeouts(ip):
    url = f'http://192.168.9.96:8000/timeouts/?ip_address={ip}'
    r = requests.get(url)
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
    url = f'http://192.168.9.96:8000/checkout/?user_id={user_id}&product_id={product_id}'
    r = requests.get(url)
    return r.json()


if __name__ == '__main__':
    import json

    cell = 11

    with open('settings.json', 'r') as conf:
        data = json.load(conf)
        # print(data)
    for items in data['cells']:
        if items['cell'] == cell:
            print(items)
        # if cell in items['cell']:
        #     print(items)
