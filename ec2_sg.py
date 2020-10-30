import argparse
from nslookup import Nslookup
import requests
import csv
import boto3


credentials_file="sg_test_eun1.csv"

#client = boto3.client(
#                'route53',
#                aws_access_key_id=args.access_key,
#                aws_secret_access_key=args.secret_key
#                )

def main():
    parser = argparse.ArgumentParser(description='Create DNS records on R53')
    #parser.add_argument('--run', type=str, choices=RUN, required=False)
    parser.add_argument('--name', type=str)
    #parser.add_argument('--type', choices=TYPE, type=str)
    parser.add_argument('--value')
    #parser.add_argument('--action', choices=ACTION)
    parser.add_argument('--ttl', default=300, type=int)
    parser.add_argument('--zone', type=str)
    parser.add_argument('--spec', default=False, type=bool)
    parser.add_argument('--access_key', type=str)
    parser.add_argument('--secret_key', type=str)

    args = parser.parse_args()

    with open(credentials_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            print(', '.join(row))




if __name__ == "__main__":
    main()