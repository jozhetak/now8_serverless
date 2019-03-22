import string
import random
import datetime
import json
import os
import boto3
import requests


RIDE_LINK_SIZE = 20

# branch.io
BRANCH_KEY = os.environ.get("BRANCH_KEY")

dynamodb = boto3.resource('dynamodb')


def main(event, context):
    ride_uid = uid_generator(RIDE_LINK_SIZE)
    join_ride_url = get_join_ride_url(ride_uid)

    ride = {
        "rideUID": ride_uid,
        "driver": "some_driver",
        "passengers": [],
        "time_created": str(datetime.datetime.now()),
        "join_ride_url": join_ride_url
    }

    rides_table_client = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    rides_table_client.put_item(Item=ride)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(ride)
    }


# Generate random string for the Ride UID
def uid_generator(random_link_size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(random_link_size))


def get_join_ride_url(ride_uid):
    branch_io_base_url = "https://api2.branch.io/v1/url"
    payload = {
        "branch_key": BRANCH_KEY,
        "data": {
            "rideUID": ride_uid
        }
    }
    new_ride_request = requests.post(branch_io_base_url, json=payload)
    new_ride_request_dictionary = new_ride_request.json()
    join_ride_url = new_ride_request_dictionary['url']

    return join_ride_url
