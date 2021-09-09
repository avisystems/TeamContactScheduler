import boto3
# import os
import json
from datetime import datetime

# variables

resp_msg = ""

# Get the service resource.
#lambda_client = boto3.client("lambda", region_name="us-east-2")
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def lambda_handler(event, context):

    try:
        sns_record = event['Records'][0]['Sns']
        sns_event_date = sns_record['Timestamp']
        sns_event_message = sns_record['Message']
        print("SNS Timestamp: {}".format(sns_event_date))
        print("SNS Message: {}".format(sns_event_message))
        date_object = datetime.strptime(sns_event_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        d1=date_object.strftime('%Y-%m-%d')
        print("D1={}".format(d1))
        d2 = '2021-09-06'
        # Get DDB Item using alert eventID and Platform (primary and sort keys on the DDB table imp-alerts)
        #ddbrecord = table.get_item(Key={'Event_ID': alert_lookup, 'Platform': alert_platform})
        #source_key = ddbrecord['Item']['Source_Key']
        # print(str(source_key))

        if d1==d2:
            print("Labor Day")
        else:
            print("Not Labor Day")

        resp_msg = "Successful invocation."

    except Exception as e:
        # Error while opening connection or processing
        print(e)
        topicARN = "arn:aws:sns:us-east-1:651699629044:SAMAppNotifications"
        subject = "PerfData - Error"
        error_msg = "Error message: %s" % str(e)
        sns_payload = {
            "_topic": topicARN,
            "_subject": subject,
            "_message": error_msg
        }
        PostSNS = boto3.client("lambda", region_name="us-east-2")
        resp = PostSNS.invoke(FunctionName="AVILIB-SNSPost-VG9gljxgIuaO",
                              InvocationType="Event",
                              Payload=json.dumps(sns_payload))
        resp_msg = "ERROR - Check the CloudWatch logs or the SNS message for details."
    finally:
        print("Closing Connection")
        print("Execution Status Message= {}".format(resp_msg))
        #if (conn is not None and conn.open):
        #    conn.close()
    return
