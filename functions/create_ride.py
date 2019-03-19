import string
import random
import datetime
import json
import os


def main(event, context):

    result = {
        "Author": "Ofir Bar",
        "App name": "now8",
        "Description": "now8 is the best app out there!",
        "Server time": str(datetime.datetime.now()),
        "Function Environment Variable": os.environ.get("FUNCTION_NAME"),
        "Provider Environment Variable": os.environ.get("PROVIDER_VARIABLE"),
        "Ride Link:": uid_generator(20)
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(result)
    }


# Generate random string for the Ride UID
def uid_generator(random_link_size, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(random_link_size))
