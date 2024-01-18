import requests
import socket


def check_user(user_number, ip):
    url = f'http://192.168.1.2:8000/check_user/?user_id={user_number}&ip_address={ip}'
    r = requests.get(url)
    return r.json()


def check_machine_status(ip):
    url = f'http://192.168.1.2:8000/vending_status/?ip_address={ip}'
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
    url = f'http://192.168.1.2:8000/checkout/?user_id={user_id}&product_id={product_id}'
    r = requests.get(url)
    return r.json()


if __name__ == '__main__':
    user_number = 12345678
    data = check_user(user_number, '192.168.7.1')
    ip_address = get_ip_address()
    print(data)
    if ip_address:
        print(f"Your IP address is: {ip_address}")
    else:
        print("Unable to retrieve IP address.")