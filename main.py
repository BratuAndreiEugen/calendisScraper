import json
import os

import requests
import time
import datetime


def parse_headers(filename: str):
    """
    Parse headers from a string into a dictionary.

    Args:
        headers_str (str): The string containing headers.

    Returns:
        dict: The parsed headers as a dictionary.
    """
    headers = {}
    with open(filename, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    return headers

def send_api_request(url, headers=None):
    """
    Sends a request to the specified API endpoint with optional headers.

    Args:
        url (str): The URL of the API endpoint.
        headers (dict): Optional headers to include in the request.

    Returns:
        response: The response object returned by requests library.
    """
    try:
        # Make the request with optional headers
        response = requests.get(url, headers=headers)

        # Print the response
        # print("Response Status Code:", response.status_code)
        # print("Response Headers:", response.headers)
        # print("Response Content:", response.text)

        return response

    except requests.exceptions.RequestException as e:
        # Handle exceptions
        print("Error:", e)

def get_unix_timestamp_midnight():
    # Get the current date
    current_date = datetime.datetime.now().date()

    # Set the time to 00:00:00
    midnight_datetime = datetime.datetime.combine(current_date, datetime.time.min)

    # Convert datetime object to Unix timestamp
    unix_timestamp = int(midnight_datetime.timestamp())
    return unix_timestamp

def increment_unix_timestamp(timestamp):
    # Add 24 hours' worth of seconds
    timestamp += 24 * 60 * 60
    return timestamp

def unix_timestamp_to_gmt(timestamp):
    # Convert Unix timestamp to datetime object
    gmt_datetime = datetime.datetime.utcfromtimestamp(timestamp)

    return gmt_datetime

def unix_timestamp_to_gmt_RO(timestamp):
    # Convert Unix timestamp to datetime object
    gmt_datetime = datetime.datetime.utcfromtimestamp(timestamp)

    # Add 3 hours to the datetime object
    gmt_datetime += datetime.timedelta(hours=3)

    return gmt_datetime


def gmt_to_unix_timestamp(gmt_date):
    # Convert GMT date to Unix timestamp
    unix_timestamp = int(gmt_date.timestamp())
    return unix_timestamp

# Get the Unix timestamp for the current day at 00:00:00
unix_timestamp_midnight = get_unix_timestamp_midnight()
# print("Unix timestamp for today at 00:00:00:", unix_timestamp_midnight)

input_str = input(" Write the days you are interested in ( separated by ; and in format DD ) : ")

date_list_str = input_str.split(';')
date_list = []
for date in date_list_str:
    date_list.append(int(date))
print(date_list)

while True:
    i = 1
    while i <= 14:
        url = "https://www.calendis.ro/api/get_available_slots?service_id=8029&location_id=1651&date=" + str(unix_timestamp_midnight) + "&day_only=1"
        custom_headers = parse_headers("header_files/header_file_1.txt")
        # print(custom_headers)

        response = send_api_request(url, headers=custom_headers)
        resp_dict = json.loads(response.text)
        available_times = resp_dict["available_slots"]
        gmt_time = unix_timestamp_to_gmt_RO(unix_timestamp_midnight)

        print(gmt_time.strftime('%D'))
        if len(available_times) != 0:
            print(gmt_time.strftime('%A') + " " + str(gmt_time))
            output_str = ""
            for slot in available_times:
                slot_str = unix_timestamp_to_gmt_RO(int(slot["time"])).strftime('%H:%M')
                output_str = output_str + "\n" + slot_str
                print(slot_str)

            day = int(gmt_time.strftime("%d"))
            print(day)
            if day in date_list:
                # Message box should be shown here
                pass

        print()
        i=i+1
        unix_timestamp_midnight = increment_unix_timestamp(unix_timestamp_midnight)

    time.sleep(30)
