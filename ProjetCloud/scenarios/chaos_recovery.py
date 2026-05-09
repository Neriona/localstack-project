import boto3
from botocore.config import Config
import json
import time
import sys
import os

# Configuration de l'encodage pour éviter les erreurs de caractères spéciaux
sys.stdout.reconfigure(encoding='utf-8')

# ===================== GESTION DES CHEMINS (CRUCIAL) =====================
# On détermine le chemin absolu du fichier created_ids.json à la racine
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
JSON_PATH = os.path.join(ROOT_DIR, "created_ids.json")

# ===================== CONFIG AWS / LOCALSTACK =====================
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
    """Charge les IDs depuis le fichier JSON à la racine du projet."""
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[OK] IDs chargés avec succès depuis : {JSON_PATH}\n")
        return data
    except FileNotFoundError:
        print(f"[ERROR] Fichier non trouvé à l'adresse : {JSON_PATH}")
        print("Avez-vous lancé le script de déploiement à la racine ?")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Erreur lors de la lecture du JSON : {e}")
        sys.exit(1)

def get_instance_status(instance_id):
    """Récupère l'état actuel d'une instance sur LocalStack."""
    try:
        resp = ec2.describe_instances(InstanceIds=[instance_id])
        return resp['Reservations'][0]['Instances'][0]['State']['Name']
    except:
        return "error"

def show_all_instances(data):
    """Affiche l'état de toutes les instances dans la console."""
    print("\n=== ÉTAT ACTUEL DE L'INFRASTRUCTURE ===")
    for iid in data.get('instance_ids', []):
        status = get_instance_status(iid)
        status_map = {
            "running": "[RUNNING]",
            "terminated": "[TERMINATED]",
            "stopped": "[STOPPED]"
        }
        color = status_map.get(status, "[UNKNOWN]")
        print(f"{color} {iid}")
    print("="*50)

def terminate_instance(instance_id):
    """Simule une panne en terminant une instance."""
    print(f"[PANNE] Simulation de crash sur l'instance : {instance_id[:12]}...")
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        # Attente de la confirmation de l'arrêt
        for _ in range(10):
            time.sleep(2)
            status = get_instance_status(instance_id)
            print(f"   Statut en cours -> {status}")
            if status == "terminated":
                print("[OK] Instance terminée avec succès.")
                return True
        return False
    except Exception as e:
        print(f"[ERROR] Échec de la terminaison : {e}")
        return False

def launch_replacement_instance(image_id="ami-df5de72bdb3b"):
    """Lance une nouvelle instance pour remplacer celle qui a crashé."""
    print("\n[RECOVERY] Lancement d'une instance de remplacement (Auto-Healing)...")
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
        print(f"[OK] Nouvelle instance créée : {new_id}")
        
        # Attente du démarrage complet
        print("Attente du statut 'running'...")
        for _ in range(15):
            time.sleep(3)
            status = get_instance_status(new_id)
            print(f"   Statut en cours -> {status}")
            if status == "running":
                print("[SUCCESS] L'instance de remplacement est opérationnelle !")
                return new_id
        return new_id
    except Exception as e:
        print(f"[ERROR] Échec du lancement : {e}")
        return None

# ===================== MAIN =====================
def main():
    # 1. Chargement des données
    data = load_ids()
    show_all_instances(data)

    if not data.get('instance_ids'):
        print("[ERROR] Aucune instance trouvée dans le fichier JSON.")
        return

    # 2. On cible la dernière instance pour le test (ex: VM3)
    target_id = data['instance_ids'][-1]
    print(f"\n[TEST] Cible du test de panne : {target_id}")

    # 3. Simulation de panne
    if terminate_instance(target_id):
        time.sleep(2)
        show_all_instances(data)

        # 4. Procédure de récupération
        print("\n[RECOVERY] Déclenchement de la procédure de récupération automatique...")
        new_id = launch_replacement_instance()

        if new_id:
            # MISE À JOUR DU FICHIER JSON (C'est ici que la magie opère pour le Dashboard)
            data['instance_ids'][-1] = new_id 
            
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                
            print(f"\n[SYNC] Le fichier {JSON_PATH} a été mis à jour.")
            print("Vérifiez votre Dashboard, l'affichage va se rafraîchir !")

    show_all_instances(data)
    print("\n=== TEST PANNE + RECOVERY TERMINÉ AVEC SUCCÈS ===")

if __name__ == "__main__":
    main()