import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

import boto3
from botocore.config import Config
import json
import time

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
    """Load infrastructure IDs"""
    try:
        with open("C:/Users/hp/ProjetCloud/created_ids.json", "r") as f:
            data = json.load(f)
        print("✅ IDs loaded successfully")
        return data
    except FileNotFoundError:
        print("✗ created_ids.json not found!")
        print("   Run your deploy_infrastructure_fixed.py first.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error reading JSON: {e}")
        sys.exit(1)


def get_instance_status(instance_id):
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        return state
    except Exception as e:
        print(f"✗ Error getting status for {instance_id}: {e}")
        return None


def stop_instance(instance_id, wait=True):
    try:
        if get_instance_status(instance_id) == "stopped":
            print(f"⚠ Instance {instance_id[:8]}... already stopped")
            return True

        print(f"⏹ Stopping instance {instance_id[:8]}...")
        ec2.stop_instances(InstanceIds=[instance_id])

        if wait:
            for i in range(40):
                time.sleep(2)
                status = get_instance_status(instance_id)
                print(f"   Status: {status}")
                if status == "stopped":
                    print(f"✓ Instance stopped successfully")
                    return True
        return True
    except Exception as e:
        print(f"✗ Error stopping: {e}")
        return False


def terminate_instance(instance_id):
    """Simule une panne brutale (Crash)"""
    try:
        print(f"💥 Terminating instance {instance_id[:8]}... (Crash simulation)")
        ec2.terminate_instances(InstanceIds=[instance_id])
        
        for i in range(30):
            time.sleep(2)
            status = get_instance_status(instance_id)
            print(f"   Status: {status}")
            if status == "terminated":
                print(f"✓ Instance terminated (crashed)")
                return True
        return False
    except Exception as e:
        print(f"✗ Error terminating: {e}")
        return False


def show_all_instances(data):
    print("\n=== 📊 All Instances Status ===")
    for instance_id in data.get('instance_ids', []):
        status = get_instance_status(instance_id)
        color = "🟢" if status == "running" else "🔴" if status == "stopped" else "⚫"
        print(f"{color} {instance_id}: {status}")
    print("="*40)


# ===================== MAIN =====================
def main():
    data = load_ids()
    
    if not data.get('instance_ids'):
        print("No instances found!")
        return

    show_all_instances(data)

    # Test sur la 2ème instance (VM2 - celle qu'on veut faire crasher)
    if len(data['instance_ids']) >= 2:
        test_id = data['instance_ids'][1]   # VM2
        print(f"\n🎯 Testing on VM2 → {test_id}")
    else:
        test_id = data['instance_ids'][0]

    # === Simulation de panne ===
    print("\n🚨 SIMULATION DE PANNE (Termination)")
    terminate_instance(test_id)

    time.sleep(3)
    show_all_instances(data)

if __name__ == "__main__":
    main()