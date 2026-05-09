import boto3
from botocore.config import Config
import json
import time
import sys
import os
from datetime import datetime

# Configuration de l'encodage pour le terminal
sys.stdout.reconfigure(encoding='utf-8')

# ===================== GESTION DES CHEMINS (CORRECTION) =====================
# On définit l'emplacement du fichier JSON par rapport à ce script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(ROOT_DIR, "created_ids.json")
LOG_FILE = os.path.join(ROOT_DIR, "monitoring_log.txt") # Log à la racine aussi

# On commente ou supprime le os.chdir qui casse tout
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ===================== CONFIG =====================
ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"
MONITORING_DURATION = 120   # 2 minutes

config = Config(read_timeout=300, connect_timeout=300)

ec2 = boto3.client('ec2', endpoint_url=ENDPOINT, region_name=REGION,
                   aws_access_key_id='test', aws_secret_access_key='test',
                   verify=False, config=config)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"Erreur écriture log: {e}")

def load_ids():
    """Charge les IDs depuis le chemin absolu calculé."""
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log(f"[ERROR] created_ids.json non trouvé à : {JSON_PATH}")
        sys.exit(1)
    except Exception as e:
        log(f"[ERROR] Lecture JSON : {e}")
        sys.exit(1)

def get_instance_status(instance_id):
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        return resp['Reservations'][0]['Instances'][0]['State']['Name']
    except:
        return "error"

def main():
    log("=== LOCALSTACK - MONITORING START ===")
    log(f"Fichier cible : {JSON_PATH}")
    
    start_time = time.time()

    try:
        while True:
            # On recharge les IDs à chaque boucle au cas où chaos-recovery a changé une instance
            data = load_ids()
            
            current_duration = int(time.time() - start_time)
            log(f"\n--- Check ({current_duration}s / {MONITORING_DURATION}s) ---")
            
            for iid in data.get('instance_ids', []):
                status = get_instance_status(iid)
                if status == "running":
                    log(f"[OK] {iid[:12]} → RUNNING")
                elif status == "terminated":
                    log(f"[PANNE DETECTÉE] {iid[:12]} → TERMINATED")
                else:
                    log(f"[WAITING] {iid[:12]} → {status}")

            if current_duration >= MONITORING_DURATION:
                log("\n=== FIN DU MONITORING (TEMPS ÉCOULÉ) ===")
                break
                
            time.sleep(8) 
            
    except KeyboardInterrupt:
        log("\n=== Monitoring arrêté par l'utilisateur ===")
    except Exception as e:
        log(f"[ERROR CRITIQUE] {e}")

    log("Fin du script.")
    print(f"\n📊 Logs sauvegardés dans : {LOG_FILE}")

if __name__ == "__main__":
    main()