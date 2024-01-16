import requests
import socket


def check_user(user_number, ip):
    url = f'http://127.0.0.1:8000/check_user/?user_id={user_number}&ip_address={ip}'
    r = requests.get(url)
    return r.json()


def get_ip_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to an external server (doesn't actually send data)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address
        ip_address = s.getsockname()[0]

        # Close the socket
        s.close()

        return ip_address

    except socket.error as e:
        print(f"Error: {e}")
        return None




if __name__ == '__main__':
    user_number = 12345678
    data = check_user(user_number, '192.168.7.1')
    ip_address = get_ip_address()
    print(data)
    if ip_address:
        print(f"Your IP address is: {ip_address}")
    else:
        print("Unable to retrieve IP address.")
