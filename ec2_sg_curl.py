import argparse
import boto3
from botocore.exceptions import ClientError
import subprocess
import json
import random

def public_ip(interface):
    ip = subprocess.getoutput(f'curl -s --interface {interface} https://checkip.amazonaws.com')
    return ip.strip()
    
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
    except ClientError as e:
        print(e)

def clear_ingress(resource, sg):
    group = resource.SecurityGroup(sg)
    group.revoke_ingress(IpPermissions=group.ip_permissions)

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--region', type=str)
    parser.add_argument('--access_key', type=str)
    parser.add_argument('--secret_key', type=str)
    parser.add_argument('--sg', type=str)
    parser.add_argument('--interface', type=str)
    parser.add_argument('--init')
    parser.add_argument('--rulesfile', type=str)

    args = parser.parse_args()
    session = boto3.session.Session(aws_access_key_id=args.access_key,
                                    aws_secret_access_key=args.secret_key,
                                    region_name = args.region
                                    )

    ec2 = session.client('ec2')
    ec2_resource = session.resource('ec2')
    publicip = public_ip(args.interface)

    with open(args.rulesfile, "r") as handler:
        json_file = json.load(handler)

    if args.init:
        json_file["previousIp"] = ""
        with open(args.rulesfile, "w") as writer:
            writer.write(json.dumps(json_file,indent=4))
    elif publicip != json_file["previousIp"]:
        print(f'IP {json_file["previousIp"]} changed to {publicip} - updating {args.sg}')
        allow_ingress(ec2, random.randint(1000, 9999), f"{publicip}/32", "temp rule", args.sg, "udp")
        clear_ingress(ec2_resource, args.sg)
        for rule in json_file["rules"]:        
            allow_ingress(ec2, rule["port"], f"{publicip}/32", rule["description"], args.sg, rule["type"])
        json_file["previousIp"] = publicip
        with open(args.rulesfile, "w") as writer:
            writer.write(json.dumps(json_file,indent=4))
    else:
        print(f'Public IP is still {json_file["previousIp"]}')
        

if __name__ == "__main__":
    main()