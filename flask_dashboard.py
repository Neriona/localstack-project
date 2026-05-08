import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, render_template, jsonify, request
import boto3
from botocore.config import Config
import json
import time

# ===================== FLASK CONFIG =====================
app = Flask(__name__, template_folder='templates')
app.config['JSON_SORT_KEYS'] = False

# ===================== AWS CONFIG =====================
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
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Loading IDs: {e}")
        return {"instance_ids": []}

def get_instance_status(instance_id):
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        state = resp['Reservations'][0]['Instances'][0]['State']['Name']
        print(f"[INFO] {instance_id[:8]}... → {state}")
        return state
    except Exception as e:
        print(f"[ERROR] Status for {instance_id}: {e}")
        return "error"

# ===================== ROUTES =====================
@app.route('/')
def dashboard():
    print("[INFO] Dashboard page requested")
    return render_template('dashboard.html')

@app.route('/api/instances')
def get_instances():
    print("[INFO] API: Getting instances...")
    data = load_ids()
    instances = []
    stats = {'running': 0, 'stopped': 0, 'terminated': 0, 'error': 0}

    for inst_id in data.get('instance_ids', []):
        status = get_instance_status(inst_id)
        instances.append({
            'id': inst_id,
            'state': status
        })
        
        if status in stats:
            stats[status] += 1
        else:
            stats['error'] += 1

    result = {
        'instances': instances,
        'total': len(instances),
        'running': stats.get('running', 0),
        'stopped': stats.get('stopped', 0),
        'terminated': stats.get('terminated', 0)
    }
    
    print(f"[INFO] Returning: {result}")
    return jsonify(result)

@app.route('/api/control', methods=['POST'])
def control_instance():
    try:
        body = request.json
        instance_id = body.get('instance_id')
        action = body.get('action')
        
        print(f"[INFO] Control request: {action} on {instance_id[:8]}...")

        if action == 'stop':
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"[OK] Stop initiated on {instance_id}")
            return jsonify({'success': True, 'message': 'Stopping instance...'})
        
        elif action == 'start':
            ec2.start_instances(InstanceIds=[instance_id])
            print(f"[OK] Start initiated on {instance_id}")
            return jsonify({'success': True, 'message': 'Starting instance...'})
        
        elif action == 'terminate':
            ec2.terminate_instances(InstanceIds=[instance_id])
            print(f"[OK] Terminate initiated on {instance_id}")
            return jsonify({'success': True, 'message': 'Terminating instance...'})
        
        else:
            return jsonify({'success': False, 'error': 'Unknown action'})
    
    except Exception as e:
        print(f"[ERROR] Control: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'service': 'LocalStack Dashboard'})

# ===================== MAIN =====================
if __name__ == '__main__':
    print("="*70)
    print(" 🚀 LOCALSTACK FAILURE SIMULATOR DASHBOARD")
    print("="*70)
    print("\n📍 Open your browser: http://localhost:5000")
    print("\nFunctionality:")
    print("  ✓ View all EC2 instances in real-time")
    print("  ✓ Monitor instance status (Running/Stopped/Terminated)")
    print("  ✓ Control instances (Stop/Start/Terminate)")
    print("  ✓ Live metrics and logs")
    print("\n" + "="*70)
    print("\nStarting Flask server...\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)