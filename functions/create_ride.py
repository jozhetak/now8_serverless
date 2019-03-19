import string
import random
import datetime
import json
import os
import boto3

RIDE_LINK_SIZE = 20
dynamodb = boto3.resource('dynamodb')


def main(event, context):

    ride_uid = uid_generator(RIDE_LINK_SIZE)
    result = {
        "Author": "Ofir Bar",
        "App name": "now8",
        "Description": "now8 is the best app out there!",
        "Server time": str(datetime.datetime.now()),
        "Function Environment Variable": os.environ.get("FUNCTION_NAME"),
        "Provider Environment Variable": os.environ.get("PROVIDER_VARIABLE"),
        "Ride Link:": ride_uid
    }

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': ride_uid,
        'text': 'This is a new ride',
        'saved to db at: ': str(datetime.datetime.now())
    }

    table.put_item(Item=item)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result)
    }


# Generate random string for the Ride UID
def uid_generator(random_link_size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(random_link_size))
