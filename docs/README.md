@"
# LocalStack - Simulation de Pannes VM Cloud

## 📋 Description

Système complet de simulation, détection et gestion des pannes de machines virtuelles dans une infrastructure Cloud pour tester la résilience du système.

**Problématique Centrale:** 
Comment simuler, détecter et gérer les pannes de VMs pour tester la résilience du système?

**Contexte:**
Les pannes VM en production causent des interruptions de service, des pertes de données et une dégradation des performances. Ce projet teste ces scénarios dans un environnement contrôlé (LocalStack) avant la mise en production.

## 👥 Équipe

- **Rayhana Laznaasni** - Créatrice Principale & Infrastructure
  - Design du système complet
  - Infrastructure et automatisation
  - Scripts Python avancés
  - Dashboard web et API REST
  
- **Chaymae Hichami Alaoui** - Co-créatrice & Tests
  - Tests et validation du système
  - Scénarios de panne
  - Collecte de métriques
  - Analyse des résultats

## 🏗️ Architecture Globale

### Infrastructure: LocalStack (AWS Simulator)

**VPC:** 10.0.0.0/16
- **Subnet:** 10.0.1.0/24
  - **EC2 Instance 1 (t2.micro)**
    - ID: i-6d99ddefd4746a5c5
    - Status: RUNNING ✓
    - IP: 10.0.1.10
  
  - **EC2 Instance 2 (t2.micro)**
    - ID: i-88e6190fe72cba224
    - Status: RUNNING ✓
    - IP: 10.0.1.11

- **Security Group:** sg-1ef99ff1d5e66b705
  - Inbound: SSH (22), HTTP (80), HTTPS (443)
  - Outbound: All traffic

### Couche Application: Python Scripts

Communiquent via Boto3 API Calls:

- **deploy_infrastructure_fixed.py** → Crée l'infrastructure
- **instance_control.py** → Contrôle manuel des instances
- **failure_recovery.py** → Simule panne + recovery automatique
- **monitoring.py** → Supervision 24/7 et logs
- **flask_dashboard.py** → Interface web

### Couche Présentation: Frontend

Via HTTP REST API:

- **Dashboard Web:** http://localhost:5000
- **Affichage des instances** en temps réel
- **Boutons:** Stop / Start / Terminate
- **Métriques** en temps réel
- **Logs d'activité**
- **Rafraîchissement auto** (10 secondes)

---

## 📦 Technologies Utilisées

| Composant | Version | Rôle |
|-----------|---------|------|
| **LocalStack** | 2026.5.0 | Émulation AWS locale |
| **Python** | 3.12 | Langage de programmation |
| **Boto3** | 1.28.0 | SDK AWS (interface API) |
| **Flask** | 2.3.0 | Framework web (backend) |
| **Docker** | 20.10+ | Conteneurisation |

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

\`\`\`bash
git clone https://github.com/Neriona/localstack-project.git
cd localstack-project
\`\`\`

#### 2️⃣ Installer les Dépendances Python

\`\`\`bash
# Créer un virtualenv
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installer les packages
pip install -r requirements.txt
\`\`\`

#### 3️⃣ Démarrer LocalStack

\`\`\`bash
docker run -d --name localstack \
  -p 4566:4566 \
  -p 4571:4571 \
  -e "SERVICES=ec2,vpc" \
  -e "DEBUG=0" \
  -e "LOCALSTACK_AUTH_TOKEN=test" \
  localstack/localstack:latest

# Attendre 30-40 secondes
# Vérifier:
curl http://localhost:4566/_localstack/health
\`\`\`

#### 4️⃣ Déployer l'Infrastructure

\`\`\`bash
python infrastructure/deploy_infrastructure_fixed.py

# Résultat attendu:
# ✓ VPC created: vpc-079e70036f64f1569
# ✓ Subnet created: subnet-eddce51717da60800
# ✓ Security Group created: sg-1ef99ff1d5e66b705
# ✓ Instance 1 created: i-6d99ddefd4746a5c5
# ✓ Instance 2 created: i-88e6190fe72cba224
\`\`\`

#### 5️⃣ Lancer le Dashboard Web

\`\`\`bash
python flask_dashboard.py

# Résultat:
# Running on http://127.0.0.1:5000
\`\`\`

**Ouvrir dans le navigateur:** http://localhost:5000

---

## 📊 Utilisation - 4 Modes de Test

### Mode 1: Dashboard Web Interactif ⭐

\`\`\`bash
python flask_dashboard.py
# Ouvrir http://localhost:5000
\`\`\`

**Avantages:**
- Interface visuelle intuitive
- Contrôle en temps réel
- Métriques affichées
- Logs en direct

---

### Mode 2: Simulation de Panne + Auto-Recovery

\`\`\`bash
python scenarios/failure_recovery.py
\`\`\`

**Résultat:**
- Instance 1: RUNNING (original)
- Instance 2: TERMINATED (crash)
- Nouvelle instance créée automatiquement
- Uptime restauré en ~30 secondes

---

### Mode 3: Monitoring Continu

\`\`\`bash
python scenarios/monitoring.py
\`\`\`

- Vérifie toutes les 8 secondes
- Logs dans monitoring_log.txt
- Durée: 2 minutes

---

### Mode 4: Contrôle Manuel Interactif

\`\`\`bash
python scenarios/instance_control.py
\`\`\`

Menu interactif:
- Show all instances
- Stop/Start/Reboot/Terminate
- Show metrics

---

## 📈 Scénarios de Panne

### Scénario 1: Arrêt Brutal (CRASH) 💥
- Détection: < 10s
- Recovery: ~30s
- Uptime après: 100%

### Scénario 2: Arrêt Gracieux (SHUTDOWN) 🔴
- Temps d'arrêt: ~6s
- Données préservées: OUI
- Redémarrage possible: OUI

### Scénario 3: Redémarrage (REBOOT) 🔄
- Temps de démarrage: ~8s
- ID conservé: OUI
- Service restauré: OUI

---

## 📊 Résultats et Métriques

| Test | Durée | Status |
|------|-------|--------|
| Déploiement infrastructure | ~15s | ✅ OK |
| Création instance 1 | ~5s | ✅ OK |
| Création instance 2 | ~5s | ✅ OK |
| Arrêt instance | ~6s | ✅ OK |
| Redémarrage instance | ~8s | ✅ OK |
| Termination instance | ~6s | ✅ OK |
| Creation replacement | ~30s | ✅ OK |
| Monitoring 2 minutes | 120s | ✅ OK |
| Dashboard Web | <1s | ✅ OK |

---

## 💡 Points Clés Réalisés

### ✅ Succès

- ✓ Infrastructure déployée automatiquement
- ✓ 2 instances EC2 réelles fonctionnelles
- ✓ VPC et Subnet configurés
- ✓ Détection de pannes automatique
- ✓ Création automatique de instances de remplacement
- ✓ Dashboard web professionnel et interactif
- ✓ Monitoring continu avec logs détaillés
- ✓ 0€ coût d'infrastructure

### ⚠️ Limitations

- ⚠️ LocalStack simule AWS
- ⚠️ Single-region
- ⚠️ Pas de stockage persistant par défaut

---

## 🎯 Améliorations Futures

1. **Load Balancer** - Distribution de charge
2. **Auto-Scaling Group** - Scaling automatique
3. **RDS Database** - Base de données
4. **Multi-région** - Failover automatique
5. **Prometheus + Grafana** - Métriques avancées

---

## 📁 Structure du Projet

\`\`\`
localstack-project/
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   └── INSTALLATION.md
├── infrastructure/
│   └── deploy_infrastructure_fixed.py
├── scenarios/
│   ├── instance_control.py
│   ├── failure_recovery.py
│   └── monitoring.py
├── templates/
│   └── dashboard.html
├── flask_dashboard.py
├── requirements.txt
└── .gitignore
\`\`\`

---

## 📞 Support

Pour l'aide:
1. Consulter [INSTALLATION.md](docs/INSTALLATION.md)
2. Vérifier les logs: \`docker logs localstack\`
3. Vérifier la santé: \`curl http://localhost:4566/_localstack/health\`

---

## 📄 Licence

**Projet Académique 2026**

Créé par:
- **Rayhana Laznaasni**
- **Chaymae Hichami Alaoui**

---

**Status:** ✅ Complet et Testé  
**Version:** 1.0.0  
**Dernière mise à jour:** 8 mai 2026
"@ | Out-File docs/README.md -Encoding UTF8
