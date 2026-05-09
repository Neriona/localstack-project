import boto3
from botocore.config import Config
import json
import time

ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"

config = Config(
    read_timeout=300,
    connect_timeout=300,
    retries={'max_attempts': 1}
)

ec2 = boto3.client(
    'ec2',
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    verify=False,
    config=config
)

def main():
    try:
        print("Creating VPC...")
        vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
        vpc_id = vpc["Vpc"]["VpcId"]
        ec2.create_tags(Resources=[vpc_id], Tags=[{"Key":"Name","Value":"demo-vpc"}])
        print(f"✓ VPC created: {vpc_id}")

        print("Creating subnet...")
        sub = ec2.create_subnet(VpcId=vpc_id, CidrBlock="10.0.1.0/24")
        subnet_id = sub["Subnet"]["SubnetId"]
        print(f"✓ Subnet created: {subnet_id}")

        print("Creating security group...")
        sg = ec2.create_security_group(GroupName="demo-sg", Description="demo", VpcId=vpc_id)
        sg_id = sg["GroupId"]
        print(f"✓ Security Group created: {sg_id}")

        print("\nCreating instances...")
        instances = []
        for i in range(2):
            try:
                print(f"  Creating instance {i+1}...")
                resp = ec2.run_instances(
                    ImageId="ami-df5de72bdb3b",
                    MinCount=1,
                    MaxCount=1,
                    InstanceType="t2.micro",
                    SubnetId=subnet_id,
                    SecurityGroupIds=[sg_id],
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [{'Key': 'Name', 'Value': f'demo-instance-{i+1}'}]
                        }
                    ]
                )
                instance_id = resp["Instances"][0]["InstanceId"]
                instances.append(instance_id)
                print(f"✓ Instance {i+1} created: {instance_id}")
            except Exception as e:
                print(f"✗ Instance {i+1} failed: {str(e)[:200]}")

        out = {
            "vpc_id": vpc_id,
            "subnet_id": subnet_id,
            "sg_id": sg_id,
            "instance_ids": instances
        }
        with open("created_ids.json", "w") as f:
            json.dump(out, f, indent=2)
        print("\n✓ Infrastructure created!")
        print(json.dumps(out, indent=2))

    except Exception as e:
        print(f"✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()