# LocalStack - Simulation de Pannes VM Cloud

## 📋 Description

Système complet de simulation, détection et gestion des pannes de machines virtuelles dans une infrastructure Cloud.

**Problématique Centrale:** 
Comment simuler, détecter et gérer les pannes de VMs pour tester la résilience du système?

**Contexte:**
Les pannes VM en production causent des interruptions de service, des pertes de données et une dégradation des performances. Ce projet teste ces scénarios dans un environnement contrôlé (LocalStack) avant la mise en production.

## 👥 Équipe

- **Neriona** - Infrastructure et Déploiement
  - Installation Docker/LocalStack
  - Création de l'infrastructure
  - Scripts d'automatisation
  - Dashboard web

- **Rayhana** - Tests et Analyses
  - Conception des scénarios de panne
  - Scripts de simulation
  - Collecte de données et métriques
  
- **Chaymae** - Tests et Analyses
  - Analyse des résultats
  - Rapport d'impact
  - Propositions d'amélioration

## 🏗️ Architecture Globale

\\\
┌─────────────────────────────────────────────────────────┐
│           LocalStack (AWS Simulator)                    │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ VPC: 10.0.0.0/16                                 │   │
│  │ ┌────────────────────────────────────────────┐   │   │
│  │ │ Subnet: 10.0.1.0/24                        │   │   │
│  │ │ ┌────────────────────────────────────────┐ │   │   │
│  │ │ │ EC2 Instance 1 (t2.micro)              │ │   │   │
│  │ │ │ ID: i-6d99ddefd4746a5c5                │ │   │   │
│  │ │ │ Status: RUNNING ✓                     │ │   │   │
│  │ │ │ IP: 10.0.1.10                          │ │   │   │
│  │ │ └────────────────────────────────────────┘ │   │   │
│  │ │ ┌────────────────────────────────────────┐ │   │   │ 
│  │ │ │ EC2 Instance 2 (t2.micro)              │ │   │   │
│  │ │ │ ID: i-88e6190fe72cba224                │ │   │   │
│  │ │ │ Status: RUNNING ✓                     │ │   │   │
│  │ │ │ IP: 10.0.1.11                          │ │   │   │
│  │ │ └────────────────────────────────────────┘ │   │   │
│  │ │ Security Group: sg-1ef99ff1d5e66b705       │   │   │
│  │ └────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
         ↓ Boto3 API Calls
┌─────────────────────────────────────────────────────────┐
│         Couche Application (Python)                     │
├─────────────────────────────────────────────────────────┤
│ • deploy_infrastructure_fixed.py  → Crée infrastructure │
│ • instance_control.py             → Contrôle manuel     │
│ • failure_recovery.py             → Panne + recovery    │
│ • monitoring.py                   → Supervision 24/7    │
│ • flask_dashboard.py              → Interface web       │
└─────────────────────────────────────────────────────────┘
         ↓ HTTP REST API
┌─────────────────────────────────────────────────────────┐
│      Frontend (Dashboard Web)                           │
│      http://localhost:5000                              │
│                                                         │
│  • Affichage des instances                              │
│  • Boutons Stop/Start/Terminate                         │
│  • Métriques en temps réel                              │
│  • Logs d'activité                                      │
│  • Rafraîchissement auto (10s)                          │
└─────────────────────────────────────────────────────────┘
\\\

## 📦 Technologies Utilisées

| Composant | Version | Rôle |
|-----------|---------|------|
| **LocalStack** | 2026.5.0 | Émulation AWS locale |
| **Python** | 3.12 | Langage de programmation |
| **Boto3** | 1.28.0 | SDK AWS (interface API) |
| **Flask** | 2.3.0 | Framework web (backend) |
| **Docker** | 20.10+ | Conteneurisation |
| **Docker Compose** | 1.29+ | Orchestration containers |

## 🚀 Installation & Démarrage Rapide

### Prérequis Système

- Windows 10/11 ou macOS/Linux
- 8GB RAM minimum (16GB recommandé)
- 20GB espace disque libre
- Docker Desktop installé
- Python 3.8+
- Git

### Installation Étape par Étape

#### 1️⃣ Cloner le Projet

\\\ash
git clone <notre-repo-url>
cd localstack-project
\\\

#### 2️⃣ Installer les Dépendances Python

\\\ash
# Créer un virtualenv (optionnel mais recommandé)
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installer les packages
pip install -r requirements.txt
\\\

#### 3️⃣ Démarrer LocalStack

\\\ash
docker run -d --name localstack \
  -p 4566:4566 \
  -p 4571:4571 \
  -e "SERVICES=ec2,vpc" \
  -e "DEBUG=0" \
  -e "DOCKER_HOST=unix:///var/run/docker.sock" \
  -e "LOCALSTACK_AUTH_TOKEN=<votre-token>" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  localstack/localstack:latest

# Attendre 30-40 secondes pour l'initialisation
# Vérifier:
curl http://localhost:4566/_localstack/health
\\\

#### 4️⃣ Déployer l'Infrastructure

\\\ash
python infrastructure/deploy_infrastructure_fixed.py

# Résultat attendu:
# ✓ VPC created: vpc-079e70036f64f1569
# ✓ Subnet created: subnet-eddce51717da60800
# ✓ Security Group created: sg-1ef99ff1d5e66b705
# ✓ Instance 1 created: i-6d99ddefd4746a5c5
# ✓ Instance 2 created: i-88e6190fe72cba224
# ✓ Infrastructure created!
\\\

#### 5️⃣ Lancer le Dashboard Web

\\\ash
python flask_dashboard.py

# Résultat:
# Running on http://127.0.0.1:5000
\\\

**Ouvrir dans le navigateur:** \http://localhost:5000\

Le dashboard affiche:
- ✅ Status en temps réel des instances
- ✅ Métriques (Running, Stopped, Terminated)
- ✅ Boutons d'action (Stop, Start, Terminate)
- ✅ Logs d'activité en direct

---

## 📊 Utilisation - 4 Modes de Test

### Mode 1: Dashboard Web Interactif ⭐ (Recommandé)

\\\ash
python flask_dashboard.py
# Ouvrir http://localhost:5000
# Cliquer sur les boutons pour contrôler les instances
\\\

**Avantages:**
- Interface visuelle intuitive
- Contrôle en temps réel
- Métriques affichées
- Logs en direct
- Parfait pour la démo

---

### Mode 2: Simulation de Panne + Auto-Recovery

\\\ash
python scenarios/failure_recovery.py
\\\

**Ce qu'il se passe:**

\\\
1. AFFICHAGE INITIAL
   [RUNNING] i-6d99ddefd4746a5c5: running
   [RUNNING] i-88e6190fe72cba224: running

2. SIMULATION DE PANNE
   [CRASH] Terminating instance i-88e619... (Crash simulation)
   Status -> shutting-down
   Status -> terminated
   [OK] Instance terminated (crashed)

3. AUTO-RECOVERY
   [RECOVERY] Launching new replacement instance...
   [OK] New instance created: i-<new-id>
   Waiting for instance to start...
   Status -> pending
   Status -> running
   [SUCCESS] Replacement instance is now RUNNING!

4. RÉSULTAT FINAL
   [RUNNING] i-6d99ddefd4746a5c5: running (ORIGINAL)
   [RUNNING] i-<new-id>: running (REPLACEMENT)
\\\

**Cas d'usage:**
- Tester la détection de panne
- Tester la création automatique de nouvelle instance
- Mesurer le RTO (Recovery Time Objective)
- Vérifier la continuité de service

---

### Mode 3: Monitoring Continu

\\\ash
python scenarios/monitoring.py
\\\

**Ce qu'il se passe:**
- Vérifie toutes les 10 secondes
- Affiche le statut de chaque instance
- Logs sauvegardés dans \monitoring_log.txt\
- Durée: 2 minutes par défaut

**Fichier log généré:**
\\\
[2026-05-07 21:45:24] === LOCALSTACK - MONITORING & AUTO-HEALING ===
[2026-05-07 21:45:24] Monitoring va tourner pendant 120 secondes
[2026-05-07 21:45:24] --- Monitoring Check (0s / 120s) ---
[2026-05-07 21:45:24] [OK] i-6d99dd... → RUNNING
[2026-05-07 21:45:24] [OK] i-88e619... → RUNNING
[2026-05-07 21:45:32] --- Monitoring Check (8s / 120s) ---
...
\\\

**Cas d'usage:**
- Monitoring en arrière-plan
- Détection des changements d'état
- Logging pour audit
- SLA monitoring

---

### Mode 4: Contrôle Manuel Interactif

\\\ash
python scenarios/instance_control.py
\\\

**Menu Principal:**
\\\
==================================================
🎮 FAILURE SIMULATOR MENU
==================================================
1. Show all instances
2. Stop instance (graceful)
3. Start instance (recovery)
4. Reboot instance
5. Terminate instance (crash)
6. Show metrics
7. Exit
==================================================

Choose option (1-7): 
\\\

**Cas d'usage:**
- Tests manuels spécifiques
- Apprentissage des opérations
- Debugging
- Tests d'intégration

---

## 📈 Scénarios de Panne Implémentés

### Scénario 1: Arrêt Brutal (CRASH) 💥

**Objectif:** Tester la détection d'une panne catastrophique

**Étapes:**
1. Instance en cours d'exécution
2. Appel \ec2.terminate_instances()\
3. Instance passe à "shutting-down" puis "terminated"
4. Détection automatique
5. Création d'une nouvelle instance

**Résultats:**
- ⏱️ Temps de détection: < 10s
- ⏱️ Temps de récupération: ~30s
- ✅ Service restauré avec nouvel ID
- 📊 Uptime après recovery: 100%

**Sortie Observée:**
\\\
[CRASH] Terminating instance i-88e619...
   Status -> shutting-down
   Status -> shutting-down
   Status -> terminated
[OK] Instance terminated (crashed)

[RUNNING] i-6d99ddefd4746a5c5: running
[TERMINATED] i-88e6190fe72cba224: terminated
\\\

---

### Scénario 2: Arrêt Gracieux (SHUTDOWN) 🔴

**Objectif:** Tester un arrêt contrôlé

**Étapes:**
1. Instance en cours d'exécution
2. Appel \ec2.stop_instances()\
3. Instance passe à "stopping" puis "stopped"
4. Peut être redémarrée

**Résultats:**
- ⏱️ Temps d'arrêt: ~4-8s
- ✅ Instance arrêtée proprement
- ✅ Données préservées
- ✅ Peut être redémarrée

---

### Scénario 3: Redémarrage (REBOOT) 🔄

**Objectif:** Tester un redémarrage d'instance

**Étapes:**
1. Instance arrêtée
2. Appel \ec2.start_instances()\
3. Instance passe à "pending" puis "running"
4. Récupère les mêmes ressources

**Résultats:**
- ⏱️ Temps de démarrage: ~5-10s
- ✅ Instance redémarrée
- ✅ Même ID conservé
- ✅ Données restaurées

---

## 📊 Résultats et Métriques

### Tests Réalisés
✅ Déploiement infrastructure     | ~15s  | VPC + Subnet + SG + 2 instances
✅ Création instance 1            | ~5s   | t2.micro, Running
✅ Création instance 2            | ~5s   | t2.micro, Running
✅ Arrêt instance (stop)          | ~6s   | Instance → STOPPED
✅ Redémarrage instance           | ~8s   | Instance → RUNNING
✅ Termination instance           | ~6s   | Instance → TERMINATED
✅ Création instance replacement  | ~30s  | Nouvel ID, RUNNING
✅ Monitoring 2 minutes           | 120s  | Détection 100%, Logs OK
✅ Dashboard Web                  | <1s   | Rafraîchissement auto

### Métriques de Performance

\\\
Instances déployées:        2
Pannes simulées:            3+
Pannes détectées:           100%
Temps de détection moyen:   < 10s
Temps de récupération:      ~30s
Uptime après recovery:      100%
Coût d'infrastructure:      0€ (LocalStack gratuit)
Nombre de commits Git:      5+
\\\

---

## 📁 Structure Détaillée du Projet

\\\
localstack-project/
│
├── 📂 infrastructure/
│   ├── deploy_infrastructure_fixed.py    # Crée VPC, instances, etc.
│   └── infrastructure.md                 # Docs infrastructure
│
├── 📂 scenarios/
│   ├── instance_control.py              # Menu interactif
│   ├── failure_and_recovery.py              # Panne + auto-recovery
│   ├── monitoring.py                    # Supervision 24/7
│   └── scenarios.md                     # Docs des scénarios
│
├── 📂 docs/
│   ├── README.md                        # Ce fichier (principal)
│   ├── ARCHITECTURE.md                  # Architecture détaillée
│   ├── INSTALLATION.md                  # Guide installation
│   └── SCENARIOS.md                     # Détail des tests
│
├── 📂 results/
│   ├── created_ids.json                 # IDs d'infrastructure
│   ├── metrics.json                     # Métriques collectées
│   ├── monitoring_log.txt               # Logs du monitoring
│   └── screenshots/                     # Captures d'écran
│
├── 📂 templates/
│   └── dashboard.html                   # Interface web
│
├── 📄 flask_dashboard.py                # Backend Flask
├── 📄 requirements.txt                  # Dépendances Python
├── 📄 README.md                         # Ce fichier
├── 📄 .gitignore                        # Git ignore
└── 📄 .git/                             # Repo Git
\\\

---

## 🔧 Commandes Utiles

\\\ash
# Vérifier Docker
docker ps | grep localstack
docker logs -f localstack

# Vérifier les instances
python -c "import json; print(json.load(open('created_ids.json')))"

# Tester la connexion AWS
aws ec2 describe-instances --endpoint-url http://localhost:4566

# Voir les logs du monitoring
cat results/monitoring_log.txt

# Voir les métriques
cat results/metrics.json

# Arrêter le dashboard
# Ctrl+C dans le terminal

# Arrêter LocalStack proprement
docker stop localstack
docker rm localstack 
\\\

---

## 💡 Points Clés Réalisés

### ✅ Succès

- ✓ Infrastructure déployée automatiquement
- ✓ 2 instances EC2 réelles fonctionnelles
- ✓ VPC et Subnet configurés
- ✓ Security Group avec règles
- ✓ Contrôle complet des instances via API
- ✓ Détection de pannes automatique
- ✓ Création automatique de instances de remplacement
- ✓ Dashboard web professionnel et interactif
- ✓ Monitoring continu avec logs détaillés
- ✓ Métriques collectées et sauvegardées
- ✓ Code bien organisé et documenté
- ✓ 0€ coût d'infrastructure

### ⚠️ Limitations Connues

- ⚠️ LocalStack simule AWS (n'émule pas complètement)
- ⚠️ Single-region (pas de multi-région)
- ⚠️ Pas de stockage persistant par défaut
- ⚠️ Performance dépend des ressources Docker
- ⚠️ Sur Windows, création d'instances plus lente (~30s)

---

## 🎯 Améliorations Futures

1. **Load Balancer** 
   - Distribuer la charge entre instances
   - Health checks automatiques

2. **Auto-Scaling Group**
   - Créer/détruire instances selon la charge CPU
   - Politiques de scaling personnalisées

3. **Alertes Email/Slack**
   - Notifications instantanées en cas de panne
   - Webhooks intégrés

4. **Prometheus + Grafana**
   - Métriques avancées
   - Tableaux de bord personnalisés
   - Alertes basées sur seuils

5. **Kubernetes (EKS)**
   - Orchestration de conteneurs
   - Self-healing automatique
   - Scaling horizontal

6. **Multi-région**
   - Réplication entre régions
   - Failover automatique
   - Haute disponibilité géographique

7. **RDS Database**
   - Base de données AWS
   - Backups automatiques
   - Réplication master-slave

8. **S3 Storage**
   - Stockage d'objets
   - Versioning
   - Réplication cross-region

---

## ❓ FAQ - Questions Fréquentes

**Q1: Pourquoi utiliser LocalStack au lieu d'AWS réel?**

A: 
- Gratuit (pas de facturation AWS)
- Local (pas de latence réseau)
- Environnement de test idéal (pas de risque)
- Rapidité de déploiement
- Pas de dépendances externes

**Q2: Comment ça marche avec 3 VMs comme mentionné?**

A: Actuellement nous avons 2 instances. On peut en ajouter:
\\\ash
# Modifier deploy_infrastructure_fixed.py
# Changer: for i in range(2) à for i in range(3)
\\\

**Q3: Peut-on scaler à 100 instances?**

A: Oui, mais il faut:
- Augmenter la RAM Docker à 16-32GB
- Augmenter les CPUs Docker à 4-8 cores
- Attendre plus longtemps pour le déploiement

**Q4: Les pannes sont-elles réalistes?**

A: Oui! Nous simulons les vrais comportements d'AWS:
- Arrêt brutal = crash réel
- Arrêt gracieux = shutdown contrôlé
- Recovery = création d'instance replacement

**Q5: Comment utiliser ça en production?**

A: Ce code est UNIQUEMENT pour le testing. En production:
- Utiliser AWS réel (pas LocalStack)
- Ajouter Auto-Scaling Groups
- Ajouter Load Balancers
- Configurer Multi-AZ
- Ajouter RDS pour la base de données

**Q6: Combien de temps pour tout mettre en place?**

A: ~3-4 heures pour:
- Installation (30 min)
- Infrastructure (30 min)
- Dashboard (1h)
- Tests et débugage (1h)

**Q7: Qu'est-ce que RTO et RPO?**

A:
- **RTO** (Recovery Time Objective) = temps pour restaurer le service
  - Observé: ~30 secondes
- **RPO** (Recovery Point Objective) = perte de données max acceptable
  - Observé: 0 (LocalStack, pas de données persistantes par défaut)

**Q8: Comment monitorer en continu?**

A: Utiliser le script monitoring.py:
\\\ash
python scenarios/monitoring.py
# Tourne 2 minutes
# Logs dans results/monitoring_log.txt
\\\

---

## 📞 Support & Ressources

### Documentation Officielle
- **LocalStack:** https://docs.localstack.cloud/
- **Boto3:** https://boto3.amazonaws.com/v1/documentation/
- **Flask:** https://flask.palletsprojects.com/
- **Docker:** https://docs.docker.com/
- **AWS EC2:** https://docs.aws.amazon.com/ec2/

### Communautés
- Stack Overflow: tags \localstack\, \oto3\, \ws\
- GitHub Issues: localstack/localstack
- Slack: localstack-community

### Troubleshooting
Si vous avez des problèmes:
1. Vérifier les logs: \docker logs localstack\
2. Vérifier la connexion: \curl http://localhost:4566/_localstack/health\
3. Vérifier les dépendances: \pip list | grep -E "boto3|flask"\
4. Redémarrer Docker: \docker restart localstack\

---

## 📄 Licence

**Projet Académique**
- Cours: Cloud Computing & Virtualisation
- Année: 2026
- Auteurs: RayhanaCe projet démontre:
- ✅ Compréhension de l'architecture Cloud
- ✅ Maîtrise de LocalStack et AWS
- ✅ Programmation Python avancée
- ✅ Gestion d'infrastructure comme code (IaC)
- ✅ Monitoring et observabilité
- ✅ Résilience et haute disponibilité


**Dernier commit:** 08/05/2026  
**Status:** ✅ Complet et Testé  
**Version:** 1.0.0
