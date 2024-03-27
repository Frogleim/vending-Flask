import time

import psycopg2
from datetime import datetime
import requests


# Function to insert data into PostgreSQL database
def get_base_url():
    try:
        conn = psycopg2.connect(
            dbname="MasterSystem",
            user="postgres",
            password="0000",
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()
        sql = """SELECT one_c_url FROM vending_app_systemsettings"""
        cursor.execute(sql)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Extract the one_c_url from the rows
        one_c_urls = [row[0] for row in rows]

        # Close cursor and connection
        cursor.close()
        conn.close()

        return one_c_urls

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None


def get_users_data():
    base_url = get_base_url()
    r = requests.get(base_url[0])
    return r.json()


def insert_data_into_db():
    # try:
    conn = psycopg2.connect(
        dbname="MasterSystem",
        user="postgres",
        password="0000",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Prepare SQL statement
    sql = """INSERT INTO vending_app_users (user_number, fio, username) 
             VALUES (%s, %s, %s)"""

    # Get current timestamp
    timestamp = datetime.now()
    data_list = get_users_data()
    # Insert each data point into the database
    for data in data_list:
        cursor.execute(sql, (int(data["passId"]), data["fio"], data["domainId"]))

    # Commit changes
    conn.commit()

    print("Data inserted successfully.")
    #
    # except (Exception, psycopg2.Error) as error:
    #     print("Error while connecting to PostgreSQL:", error)
    #
    # finally:
    #     if conn:
    #         cursor.close()
    #         conn.close()
    #         print("PostgreSQL connection is closed.")


if __name__ == "__main__":
    while True:
        insert_data_into_db()
        time.sleep(24*3600)