import argparse
import requests
import csv
import boto3
from botocore.exceptions import ClientError

def public_ip():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    return ip
    
def allow_ingress(client, port, ip, comment, sg, udptcp):
    try:
        data = client.authorize_security_group_ingress(
        GroupId=sg,
        IpPermissions=[
            {'IpProtocol': udptcp,
             'FromPort': port,
             'ToPort': port,
             'IpRanges': [
                {'CidrIp': ip,
                'Description': comment}
             ]
            }
        ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)

def clear_ingress(resource, sg):
    group = resource.SecurityGroup(sg)
    group.revoke_ingress(IpPermissions=group.ip_permissions)

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--port', type=int)
    parser.add_argument('--udptcp', type=str)
    parser.add_argument('--region', type=str)
    parser.add_argument('--description', type=str)
    parser.add_argument('--access_key', type=str)
    parser.add_argument('--secret_key', type=str)
    parser.add_argument('--sg', type=str)

    args = parser.parse_args()
    session = boto3.session.Session(aws_access_key_id=args.access_key,
                                    aws_secret_access_key=args.secret_key,
                                    region_name = args.region
                                    )

    ec2 = session.client('ec2')
    ec2_resource = session.resource('ec2')
    publicip = public_ip()

    with open("publicip.txt", "r") as handler:
        publicip_writen = handler.read()

    if publicip != publicip_writen:
        print(f'IP {publicip_writen} changed to {publicip} - updating {args.sg}')
        clear_ingress(ec2_resource, args.sg)
        allow_ingress(ec2, args.port, f"{publicip}/32", args.description, args.sg, args.udptcp)
        with open("publicip.txt", "w") as writer:
            writer.write(publicip)
    else:
        print(f'Public IP is still {publicip_writen}')
        




if __name__ == "__main__":
    main()