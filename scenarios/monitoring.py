import boto3
from botocore.config import Config
import json
import time
import sys
import os
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

# ===================== CONFIG =====================
ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"
MONITORING_DURATION = 120   # Durée totale du monitoring en secondes (2 minutes par défaut)

config = Config(read_timeout=300, connect_timeout=300)

ec2 = boto3.client('ec2', endpoint_url=ENDPOINT, region_name=REGION,
                   aws_access_key_id='test', aws_secret_access_key='test',
                   verify=False, config=config)

LOG_FILE = "monitoring_log.txt"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_ids():
    try:
        with open("created_ids.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        log("[ERROR] created_ids.json not found!")
        sys.exit(1)


def get_instance_status(instance_id):
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        return resp['Reservations'][0]['Instances'][0]['State']['Name']
    except:
        return "error"


def main():
    log("=== LOCALSTACK - MONITORING & AUTO-HEALING (FINAL VERSION) ===")
    log(f"Monitoring va tourner pendant {MONITORING_DURATION} secondes")
    
    data = load_ids()
    start_time = time.time()

    try:
        while True:
            current_duration = int(time.time() - start_time)
            log(f"\n--- Monitoring Check ({current_duration}s / {MONITORING_DURATION}s) ---")
            
            for iid in data.get('instance_ids', []):
                status = get_instance_status(iid)
                if status == "running":
                    log(f"[OK] {iid[:8]}... → RUNNING")
                elif status == "terminated":
                    log(f"[PANNE DETECTÉE] {iid[:8]}... → TERMINATED")
                    # Auto-recovery (tu peux l'activer ici)
                else:
                    log(f"[WARNING] {iid[:8]}... → {status}")

            if current_duration >= MONITORING_DURATION:
                log("\n=== FIN DU MONITORING ===")
                break
                
            time.sleep(8)   # Check toutes les 8 secondes
            
    except KeyboardInterrupt:
        log("\n=== Monitoring arrêté manuellement ===")
    except Exception as e:
        log(f"[ERROR] {e}")

    log("Monitoring terminé.")
    print(f"\n📊 Logs sauvegardés dans : {LOG_FILE}")

if __name__ == "__main__":
    main()