import requests
import socket


def check_user(user_number, ip):
    url = f'http://192.168.18.110:8000/check_user/?user_id={user_number}&ip_address={ip}'
    r = requests.get(url)
    return r.json()


def check_machine_status(ip):
    url = f'http://192.168.18.110:8000/vending_status/?ip_address={ip}'
    r = requests.get(url)
    return r.json()


def change_machine_status(ip):
    url = f'http://192.168.18.110:8000/change_status/?ip_address={ip}'
    r = requests.get(url)
    return r.json()

def get_timeouts(ip):
    url = f'http://192.168.18.110:8000/timeouts/?ip_address={ip}'
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
    url = f'http://192.168.18.110:8000/checkout/?user_id={user_id}&product_id={product_id}'
    r = requests.get(url)
    return r.json()


if __name__ == '__main__':
    import pandas as pd

# Read the DataFrame from the Excel file
    excel_file_path = './grid-export (1).xlsx'
    df = pd.read_excel(excel_file_path)

    # Replace missing or non-finite values with a default value (e.g., 0)
    df['start'] = df['start'].fillna(0).astype(int)
    df['end'] = df['end'].fillna(0).astype(int)

    # Define the check range
    check_start = df['start'].min()
    check_end = df['end'].max()

    # Generate a range of numbers from 'check_start' to 'check_end'
    all_numbers_check = set(range(check_start, check_end + 1))

    # Get the list of unique numbers in the 'start' and 'end' columns
    existing_numbers_check = set(df['start']).union(df['end'])

    # Find the missing numbers in the check range
    missing_numbers_check = all_numbers_check - existing_numbers_check

    print("Missing Numbers in Check Range:", missing_numbers_check)
