import string
import random
import datetime
import json
import os
import boto3
import requests

# branch.io

RIDE_LINK_SIZE = 20

BRANCH_KEY = os.environ.get("BRANCH_KEY")

dynamodb = boto3.resource('dynamodb')


def main(event, context):
    print("Branch Key: " + str(BRANCH_KEY))
    ride_uid = uid_generator(RIDE_LINK_SIZE)
    result = {
        "rideUID": ride_uid,
        "driver": "some_driver",
        "passengers:": [],
        "time_created": str(datetime.datetime.now()),
    }

    rides_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    ride = {
        'id': ride_uid,
        'driver': 'Some Driver ID',
        'passengers': [],
        'time_created': str(datetime.datetime.now())
    }

    rides_table.put_item(Item=ride)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result)
    }


# Generate random string for the Ride UID
def uid_generator(random_link_size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(random_link_size))
