import boto3
import json
import logging
import os

dynamodb = boto3.resource('dynamodb')

HARD_CODED_RIDE_UID_FOR_TESTING = "NZJs40Nts2ShOXfk29JI" # A hard-coded rideUID, that exists in DynamoDB, for testing only.

def main(event, context):


#TODO: Throw exception if the event from API Gateway didn't sent a rideUID String

#    data = json.loads(event['body'])
#    if 'rideUID' not in data:
#        logging.error("Join ride request must include the rideUID")
#        raise Exception("Couldn't update the passengers in this ride")
#        return

    rides_table_client = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    # ride_uid = data["rideUID"]

    ride_uid = HARD_CODED_RIDE_UID_FOR_TESTING  # TODO: Change this to get the rideUID from the event, right now the rideUID is hard-coded

    # Updates the "passengers" attribute in a specific rideUID item, in dynamoDB
    response = rides_table_client.update_item(
        TableName='now8-dev',  # TODO: change the TableName to retrieve it automatically, and don't hardcode now8-dev.
        Key={
            'rideUID': ride_uid
        },
        UpdateExpression="set #passengersList = list_append(#passengersList, :newPassengerValue)",
        ExpressionAttributeNames={
            '#passengersList': 'passengers'
        },
        ExpressionAttributeValues={
            ':newPassengerValue': ["DuduAharon"]  # TODO: add a dynamic username here (of the newly joined passenger)
        },
        ReturnValues="UPDATED_NEW"
    )

    return{
        'statusCode': 200,
        'body': json.dumps(response)
    }
