import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')


def main(event, context):
    print(event)
    print("type of event:" + str(type(event)))
    data = event['queryStringParameters']  # SEX !!! JUST TO GRAB UR ATTENTION
    print("type of data:" + str(type(data)))

    if 'rideUID' not in data:
        print("Join ride request must include the rideUID")
        raise Exception("Couldn't update the passengers in this ride, no rideUID found")
    print("RideUID in Data: " + data.get('rideUID'))

    rides_table_client = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    ride_uid = data.get('rideUID')
    print("type of ride_uid:" + str(type(ride_uid)))
    print("ride uid: " + ride_uid)

    # Updates the "passengers" attribute in a specific rideUID item, in dynamoDB
    response = rides_table_client.update_item(
        TableName='now8-dev',
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
