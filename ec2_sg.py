import argparse
import requests
import csv
import boto3

CRED = ['file',
        'parameters',
        'host']

global client
client = boto3.client('ec2')

def credentials():
    client = boto3.client('ec2')
    client = boto3.client('ec2',
                           aws_access_key_id=args.access_key,
                           aws_secret_access_key=args.secret_key
                         )

def read_sg():


def public_ip():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    return ip

def main():
    parser = argparse.ArgumentParser(description='Create DNS records on R53')
    #parser.add_argument('--run', type=str, choices=RUN, required=False)
    parser.add_argument('--name', type=str)
    parser.add_argument('--cred', choices=CRED, type=str)
    parser.add_argument('--file', type=str)
    parser.add_argument('--value')
    #parser.add_argument('--action', choices=ACTION)
    parser.add_argument('--ttl', default=300, type=int)
    parser.add_argument('--zone', type=str)
    parser.add_argument('--spec', default=False, type=bool)
    parser.add_argument('--access_key', type=str)
    parser.add_argument('--secret_key', type=str)

    args = parser.parse_args()

    with open(args.file, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            print(row['Access key ID'])
            print(row['Secret access key'])
        




if __name__ == "__main__":
    main()