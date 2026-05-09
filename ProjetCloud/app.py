import sys
import os
import json
from flask import Flask, render_template, jsonify, request
import boto3
from botocore.config import Config

# Configuration du dossier de travail et de l'encodage
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# ===================== CONFIGURATION LOCALSTACK =====================
ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"

config = Config(read_timeout=120, connect_timeout=120)

ec2 = boto3.client(
    'ec2',
    endpoint_url=ENDPOINT,
    region_name=REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    verify=False,
    config=config
)

# ===================== FONCTIONS UTILES =====================

def load_ids():
    """Charge les instances depuis le fichier JSON généré par le déploiement."""
    try:
        if os.path.exists("created_ids.json"):
            with open("created_ids.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {"instance_ids": []}
    except Exception as e:
        print(f"❌ Erreur JSON : {e}")
        return {"instance_ids": []}

def get_instance_info(instance_id):
    """Récupère les détails d'une instance via Boto3."""
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        inst = resp['Reservations'][0]['Instances'][0]
        return {
            'id': instance_id,
            'state': inst['State']['Name'],
            'type': inst['InstanceType']
        }
    except:
        return {'id': instance_id, 'state': 'error', 'type': 'unknown'}

# ===================== ROUTES FLASK =====================

@app.route('/')
def index():
    """Route principale affichant index.html."""
    data = load_ids()
    instances_list = []
    stats = {'total': 0, 'running': 0, 'stopped': 0, 'terminated': 0}

    for iid in data.get('instance_ids', []):
        info = get_instance_info(iid)
        instances_list.append(info)
        stats['total'] += 1
        if info['state'] in stats:
            stats[info['state']] += 1

    return render_template('index.html', instances=instances_list, stats=stats)

@app.route('/api/instances')
def api_instances():
    """Mise à jour dynamique (AJAX) des données."""
    data = load_ids()
    instances_list = [get_instance_info(iid) for iid in data.get('instance_ids', [])]
    stats = {
        'total': len(instances_list),
        'running': sum(1 for i in instances_list if i['state'] == 'running'),
        'stopped': sum(1 for i in instances_list if i['state'] == 'stopped'),
        'terminated': sum(1 for i in instances_list if i['state'] == 'terminated')
    }
    return jsonify({'instances': instances_list, 'stats': stats})

@app.route('/api/control', methods=['POST'])
def control():
    """Route pour piloter les instances (Start/Stop/Kill)."""
    data = request.json
    iid = data.get('instance_id')
    action = data.get('action')
    try:
        if action == 'start':
            ec2.start_instances(InstanceIds=[iid])
        elif action == 'stop':
            ec2.stop_instances(InstanceIds=[iid])
        elif action == 'terminate':
            ec2.terminate_instances(InstanceIds=[iid])
        return jsonify({'success': True, 'message': f"Action {action} réussie sur {iid[:8]}"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'location': 'Beni Mellal'})

if __name__ == '__main__':
    print("🚀 Dashboard prêt sur http://127.0.0.1:5005")
    app.run(debug=False, port=5005)