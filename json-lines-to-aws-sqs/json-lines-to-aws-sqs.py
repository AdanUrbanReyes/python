import sys
import json
import boto3

file_path = 'input-test'
sqs_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue-name'
sqs_client = boto3.client('sqs')

def send(line):
    try:
        message = json.loads(line)
        response = sqs_client.send_message(
            QueueUrl=sqs_url,
            MessageBody=line,
            DelaySeconds=11
        )
        print(f"{message} sended {response['MessageId']}")
    except Exception as e:
        print(f"unable to send {line} {e}")

def main():
    try:
        with open(file_path, 'r') as file:
            for line in file:
                send(line.strip())
    except FileNotFoundError:
        print(f"{file_path} was not found.")
    except Exception as e:
        print(f"unable to read {e}")

if len(sys.argv) == 3:
    file_path = sys.argv[1]
    sqs_url = sys.argv[2]
    main()
else:
    print(f"exeucte script as {sys.argv[0]} ${{file_path}} ${{sqs_url}}")

