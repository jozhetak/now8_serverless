import json
import datetime


def main(event, context):
    current_time = datetime.datetime.now().time()

    body = {
        "message": "Current server time is: " + str(current_time)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
