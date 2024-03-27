import psycopg2
import time
import subprocess
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)


def read_config_file():
    with open(os.path.join(parent_dir, 'config.json')) as config_file:
        return json.load(config_file)


def ping_urls():
    data = read_config_file()
    try:
        command = ['ping', '-c', '1', data["controller_api_url"]]
        result = subprocess.run(command, stdout=subprocess.PIPE)
        if result.returncode != 0:
            print(f"{data['controller_api_url']} is unreachable")


        else:
            print(data['controller_api_url'])
            print(f"{data['controller_api_url']} is reachable")

    except Exception as e:
        print(f"Error pinging {data['controller_api_url']}: {e}")


if __name__ == "__main__":
    while True:
        ping_urls()
        time.sleep(3600)
