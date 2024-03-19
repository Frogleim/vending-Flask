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


# if __name__ == '__main__':
#     # import pandas as pd
#     #
#     # # Read the DataFrame from the Excel file
#     # excel_file_path = './grid-export (1).xlsx'
#     # df = pd.read_excel(excel_file_path)
#     #
#     # # Replace missing or non-finite values with a default value (e.g., 0)
#     # df['start'] = df['start'].fillna(0).astype(int)
#     # df['end'] = df['end'].fillna(0).astype(int)
#     #
#     # # Define the check range
#     # check_start = df['start'].min()
#     # check_end = df['end'].max()
#     #
#     # # Generate a range of numbers from 'check_start' to 'check_end'
#     # all_numbers_check = set(range(check_start, check_end + 1))
#     #
#     # # Get the list of unique numbers in the 'start' and 'end' columns
#     # existing_numbers_check = set(df['start']).union(df['end'])
#     #
#     # # Find the missing numbers in the check range
#     # missing_numbers_check = all_numbers_check - existing_numbers_check
#     #
#     # print("Missing Numbers in Check Range:", missing_numbers_check)

#     print(parent_dir)
#     data = read_config_file()
#     print(data)
