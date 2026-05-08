import boto3
from botocore.config import Config
import json
import time
import sys
import os

# Force UTF-8 encoding
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

# ===================== CONFIG =====================
ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"

config = Config(read_timeout=300, connect_timeout=300)

ec2 = boto3.client(
    'ec2',
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    verify=False,
    config=config
)

# ===================== FUNCTIONS =====================
def load_ids():
    try:
        with open("created_ids.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print("[OK] Infrastructure IDs loaded successfully\n")
        return data
    except FileNotFoundError:
        print("[ERROR] created_ids.json not found!")
        print("   Please run deploy_infrastructure.py first.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Reading JSON: {e}")
        sys.exit(1)


def get_instance_status(instance_id):
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        return resp['Reservations'][0]['Instances'][0]['State']['Name']
    except:
        return "error"


def show_all_instances(data):
    print("\n=== CURRENT INSTANCES STATUS ===")
    for iid in data.get('instance_ids', []):
        status = get_instance_status(iid)
        if status == "running":
            color = "[RUNNING]"
        elif status == "terminated":
            color = "[TERMINATED]"
        elif status == "stopped":
            color = "[STOPPED]"
        else:
            color = "[UNKNOWN]"
        print(f"{color} {iid}")
    print("="*50)


def terminate_instance(instance_id):
    print(f"[PANNE] Terminating instance {instance_id[:8]}... (Crash simulation)")
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        
        for _ in range(15):
            time.sleep(2)
            status = get_instance_status(instance_id)
            print(f"   Status -> {status}")
            if status == "terminated":
                print("[OK] Instance terminated successfully")
                return True
        return False
    except Exception as e:
        print(f"[ERROR] Termination failed: {e}")
        return False


def launch_replacement_instance(image_id="ami-df5de72bdb3b"):
    print("\n[RECOVERY] Launching new replacement instance...")
    
    try:
        response = ec2.run_instances(
            ImageId=image_id,
            InstanceType="t2.micro",
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'VM-Replacement-AutoHealing'}]
            }]
        )
        
        new_id = response['Instances'][0]['InstanceId']
        print(f"[OK] New instance created: {new_id}")
        
        print("Waiting for instance to start...")
        for _ in range(25):
            time.sleep(3)
            status = get_instance_status(new_id)
            print(f"   Status -> {status}")
            if status == "running":
                print("[SUCCESS] Replacement instance is now RUNNING !")
                return new_id
        print("[WARNING] Instance created but not running quickly")
        return new_id
    except Exception as e:
        print(f"[ERROR] Failed to launch replacement: {e}")
        return None


# ===================== MAIN =====================
def main():
    data = load_ids()
    show_all_instances(data)

    if not data.get('instance_ids'):
        print("[ERROR] No instances found!")
        return

    # Take the last instance as target (usually VM3)
    target_id = data['instance_ids'][-1]
    print(f"\n[TEST] Target instance for failure test: {target_id}")

    # === 1. Simulate Failure ===
    terminate_instance(target_id)
    time.sleep(3)
    show_all_instances(data)

    # === 2. Recovery (Auto-healing) ===
    print("\n[RECOVERY] Starting automatic recovery procedure...")
    new_id = launch_replacement_instance()

    if new_id:
        # Update JSON file
        data['instance_ids'][-1] = new_id
        with open("created_ids.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("[OK] created_ids.json updated with new instance")

    show_all_instances(data)
    print("\n=== TEST PANNE + RECOVERY COMPLETED ===")

if __name__ == "__main__":
    main()
    