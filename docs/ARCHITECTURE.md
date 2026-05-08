# Architecture Detaillee - LocalStack Failure Simulator

## Composants Principaux

L'architecture est organisee en trois couches:

1. Infrastructure (LocalStack/AWS)
2. Application (Scripts Python)
3. Presentation (Dashboard Web)

## Infrastructure AWS

### VPC (Virtual Private Cloud)

ID: vpc-079e70036f64f1569
CIDR: 10.0.0.0/16
Etat: Active
Role: Reseau virtuel isole

### Subnet

ID: subnet-eddce51717da60800
CIDR: 10.0.1.0/24
Zone: us-east-1a
VPC Parent: vpc-079e70036f64f1569

### Security Group

ID: sg-1ef99ff1d5e66b705

Regles Entrantes:
- SSH (TCP 22)
- HTTP (TCP 80)
- HTTPS (TCP 443)

Regles Sortantes:
- Tous les ports, tous les protocoles

### EC2 Instances

Instance 1:
  ID: i-6d99ddefd4746a5c5
  Type: t2.micro
  vCPU: 1
  RAM: 512 MB
  IP: 10.0.1.10
  Etat: RUNNING

Instance 2:
  ID: i-88e6190fe72cba224
  Type: t2.micro
  vCPU: 1
  RAM: 512 MB
  IP: 10.0.1.11
  Etat: RUNNING

## Couche Application

### Technologies

LocalStack: 2026.5.0 - Emulation AWS
Python: 3.12 - Langage de programmation
Boto3: 1.28.0 - SDK AWS
Flask: 2.3.0 - Framework web
Docker: 20.10+ - Containerisation

### Modules Python

deploy_infrastructure_fixed.py:
- Cree VPC, Subnet, Security Group
- Lance 2 instances EC2
- Sauvegarde les IDs dans created_ids.json
- Duree: ~15 secondes

instance_control.py:
- Menu interactif pour contrôler les instances
- Options: Show, Stop, Start, Reboot, Terminate, Metrics
- Utilisation: Tests manuels

failure_recovery.py:
- Simule une panne (terminate instance)
- Cree automatiquement une nouvelle instance
- Met a jour created_ids.json
- Duree: ~30-40 secondes

monitoring.py:
- Verifie l'etat toutes les 8 secondes
- Logs dans monitoring_log.txt
- Duree: 2 minutes par defaut
- Detecte automatiquement les pannes

flask_dashboard.py:
- Serveur web Flask sur port 5000
- API REST endpoints
- Affiche les instances en temps reel
- Permet le contrôle via boutons

## Couche Presentation

Dashboard Web:
- URL: http://localhost:5000
- Affichage instances en temps reel
- Metriques (Running, Stopped, Terminated)
- Boutons d'action (Stop, Start, Terminate)
- Logs d'activite en direct
- Rafraichissement auto (10 secondes)

Technologie: HTML5 + CSS3 + JavaScript Vanilla

## Flux de Donnees

Scenario 1: Affichage des instances
1. Utilisateur ouvre http://localhost:5000
2. Flask retourne dashboard.html
3. JavaScript: fetch('/api/instances')
4. Flask appelle: ec2.describe_instances()
5. LocalStack retourne le status
6. HTML affiche les instances
7. Rafraichissement auto toutes les 10 secondes
Duree: < 1 seconde

Scenario 2: Arreter une instance
1. Utilisateur clique bouton STOP
2. JavaScript: POST /api/control
3. Flask reçoit: {instance_id, action: stop}
4. Flask appelle: ec2.stop_instances()
5. Instance: RUNNING → STOPPING → STOPPED
6. JavaScript rafraichit le dashboard
7. Nouvel etat affiché: STOPPED
Duree: ~6-8 secondes

Scenario 3: Panne + Recovery
1. failure_recovery.py lance
2. Appel: ec2.terminate_instances()
3. Instance: RUNNING → SHUTTING-DOWN → TERMINATED
4. Nouvelle instance creee
5. Nouvelle instance: PENDING → RUNNING
6. created_ids.json mise a jour
7. Dashboard affiche la nouvelle instance
Duree: ~30-40 secondes

## Fichiers de Configuration

created_ids.json:
- Stocke les IDs d'infrastructure
- Utilise par tous les scripts
- Structure:
  {
    "vpc_id": "vpc-...",
    "subnet_id": "subnet-...",
    "security_group_id": "sg-...",
    "instance_ids": ["i-...", "i-..."]
  }

metrics.json:
- Collecte les metriques de panne
- Stocke l'historique des failures
- Utilisé pour l'analyse

monitoring_log.txt:
- Logs de tous les events
- Timestamp pour chaque verification
- Utilisé pour l'audit

## Cycle de Vie d'une Instance

CREATION (deploy_infrastructure.py)
    |
    v
PENDING (en cours de demarrage)
    |
    v
RUNNING (prete)
    |
    +-- STOP (arret gracieux)
    |    |
    |    v
    |   STOPPING
    |    |
    |    v
    |   STOPPED
    |    |
    |    v
    |   START (redemarrage)
    |    |
    |    v
    |   RUNNING
    |
    +-- TERMINATE (crash)
         |
         v
    SHUTTING-DOWN
         |
         v
    TERMINATED
         |
         v
    (Nouvelle instance creee)

## Metriques de Performance

Temps d'execution par operation:
- Creer instance: ~5 secondes
- Arreter instance: ~6 secondes
- Redemarrer instance: ~8 secondes
- Terminer instance: ~6 secondes
- Auto-recovery total: ~30 secondes
- Dashboard refresh: <1 seconde
- Monitoring check: <1 seconde

Ressources utilisees:
- Docker (LocalStack): 10-20% CPU, 800MB-1.2GB RAM
- Python (Scripts): 1-5% CPU, 50-100MB RAM
- Flask Dashboard: <1% CPU idle, 30MB RAM

## Concepts de Resilience

RTO (Recovery Time Objective):
- Temps maximal pour restaurer un service
- Arret gracieux: ~6 secondes
- Arret brutal + recovery: ~36 secondes
- Accepte pour la plupart des applications

RPO (Recovery Point Objective):
- Perte de donnees acceptable
- LocalStack: RPO = 0 (pas de donnees persistantes)
- En production: A configurer avec EBS, RDS, etc.

Uptime:
- Avant panne: 100%
- Pendant panne: 0%
- Apres recovery: 100%

## Points de Integration

Boto3 <-> LocalStack:
- Endpoint: http://localhost:4566
- Authentification: AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY
- Region: us-east-1

Flask <-> Frontend:
- Port: 5000
- Endpoints: /, /api/instances, /api/control, /health
- Format: JSON

Python <-> AWS:
- Tous les scripts utilisent Boto3
- Appels API synchrones
- Gestion des erreurs avec try/except

## Limitations Connues

- LocalStack simule AWS (pas une vraie emulation)
- Single-region uniquement
- Pas de persistence de donnees par defaut
- Performance limitee par les ressources de la machine
- Sur Windows, creation d'instances plus lente

## Améliorations Futures

Load Balancer:
- Distribuer la charge entre instances
- Health checks automatiques

Auto-Scaling Group:
- Creer/detruire instances selon la charge CPU
- Politiques de scaling personnalisees

RDS Database:
- Persistence des donnees
- Backups automatiques
- Replication master-slave

Kubernetes:
- Orchestration de conteneurs
- Self-healing automatique
- Scaling horizontal

Multi-Region:
- Replication entre regions
- Failover automatique
- Haute disponibilite geographique

Prometheus + Grafana:
- Metriques avancees
- Tableaux de bord personnalises
- Alertes basees sur seuils

## Securite et Isolation

Network Isolation:
- VPC prive: 10.0.0.0/16
- Subnet prive: 10.0.1.0/24
- Security Group: Contrôle d'acces

API Access:
- LocalStack: Endpoint local uniquement
- Pas d'acces reseau externe
- Pas de vraies donnees AWS

Data Protection:
- Pas de donnees sensibles stockees
- LocalStack: Memoire ephemere
- created_ids.json: Seulement les IDs

## Extensibilite

Pour ajouter RDS:
rds = boto3.client('rds', endpoint_url=ENDPOINT)
rds.create_db_instance(...)

Pour ajouter Load Balancer:
elb = boto3.client('elbv2', endpoint_url=ENDPOINT)
elb.create_load_balancer(...)

Pour ajouter Auto-Scaling:
asg = boto3.client('autoscaling', endpoint_url=ENDPOINT)
asg.create_auto_scaling_group(...)

## Conclusion

Cette architecture demontre:
- Comprehension de l'architecture Cloud
- Gestion et automation d'infrastructure
- Monitoring et observabilite
- Resilience et haute disponibilite
- Interface utilisateur intuitive

Le design separe les responsabilites (infrastructure, application, presentation) et permet une extensibilite future facile.

---

Derniere mise a jour: 7 mai 2026
Version: 1.0
Statut: Complet et Teste
