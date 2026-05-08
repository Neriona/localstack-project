# Guide d'Installation Complet - LocalStack Failure Simulator

## 📋 Table des Matières

1. Prérequis Système
2. Installation Étape par Étape
3. Vérification de l'Installation
4. Dépannage
5. Commandes Utiles
6. Prochaines Étapes

---

## 🖥️ Prérequis Système

### Matériel Minimum

- **Processeur:** Intel/AMD multi-cœur (2+ cœurs)
- **RAM:** 8GB minimum (16GB recommandé)
- **Disque dur:** 20GB d'espace libre
- **Réseau:** Connexion Internet pour télécharger les images

### Système d'Exploitation

- Windows 10/11 (64-bit)
- macOS 10.15+ (Intel ou Apple Silicon)
- Linux (Ubuntu 20.04+, Debian, CentOS, etc.)

### Logiciels Requis

| Logiciel | Version | Lien |
|----------|---------|------|
| Python | 3.8+ | https://www.python.org/downloads/ |
| Docker Desktop | 20.10+ | https://www.docker.com/products/docker-desktop |
| Git | 2.25+ | https://git-scm.com/downloads |
| Visual Studio Code | Optionnel | https://code.visualstudio.com/ |

---

## ⚙️ Installation Étape par Étape

### ÉTAPE 1: Installer Python

#### Windows

1. Télécharger Python depuis https://www.python.org/downloads/
2. **Important:** Cocher "Add Python to PATH"
3. Cliquer "Install Now"
4. Vérifier l'installation:

\\\powershell
python --version
pip --version
\\\

Résultat attendu:
\\\
Python 3.12.0
pip 23.2.1
\\\

#### macOS

\\\ash
# Avec Homebrew
brew install python3

# Vérifier
python3 --version
pip3 --version
\\\

#### Linux (Ubuntu/Debian)

\\\ash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Vérifier
python3 --version
pip3 --version
\\\

---

### ÉTAPE 2: Installer Docker Desktop

#### Windows

1. Télécharger depuis https://www.docker.com/products/docker-desktop
2. Exécuter l'installateur
3. **Important:** Cocher "WSL 2" (Windows Subsystem for Linux 2)
4. Redémarrer l'ordinateur
5. Vérifier:

\\\powershell
docker --version
docker run hello-world
\\\

Résultat attendu:
\\\
Docker version 20.10.21
Hello from Docker!
\\\

#### macOS

1. Télécharger depuis https://www.docker.com/products/docker-desktop
2. Drag and drop dans Applications
3. Lancer Docker depuis Applications
4. Vérifier:

\\\ash
docker --version
docker run hello-world
\\\

#### Linux

\\\ash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker \

# Vérifier
docker --version
docker run hello-world
\\\

---

### ÉTAPE 3: Installer Git

#### Windows

1. Télécharger depuis https://git-scm.com/downloads
2. Utiliser les options par défaut
3. Redémarrer le terminal
4. Vérifier:

\\\powershell
git --version
\\\

#### macOS

\\\ash
brew install git
git --version
\\\

#### Linux

\\\ash
sudo apt install git
git --version
\\\

---

### ÉTAPE 4: Cloner le Projet

\\\ash
# Créer un dossier pour le projet
mkdir localstack-projects
cd localstack-projects

# Cloner le dépôt (remplacer par votre URL)
git clone <votre-repo-url>
cd localstack-project

# Vérifier la structure
ls -la
\\\

Résultat attendu:
\\\
infrastructure/
scenarios/
docs/
results/
templates/
flask_dashboard.py
requirements.txt
README.md
.gitignore
\\\

---

### ÉTAPE 5: Créer un Environnement Virtuel Python

#### Windows

\\\powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
venv\Scripts\activate

# Vérifier (vous devez voir (venv) au début de la ligne)
# (venv) C:\Users\...>
\\\

#### macOS/Linux

\\\ash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Vérifier (vous devez voir (venv) au début)
# (venv) user@machine:~$
\\\

---

### ÉTAPE 6: Installer les Dépendances Python

\\\ash
# L'environnement virtuel DOIT être activé

# Upgrade pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Vérifier
pip list
\\\

Résultat attendu:
\\\
boto3             1.28.0
botocore          1.31.0
Flask             2.3.0
python-dotenv     1.0.0
requests          2.31.0
\\\

---

### ÉTAPE 7: Obtenir un Token LocalStack (Gratuit)

\\\
1. Aller sur https://app.localstack.cloud/sign-up
2. Se connecter avec GitHub ou créer un compte
3. Aller dans Settings
4. Copier le LOCALSTACK_AUTH_TOKEN
5. Garder ce token à portée de main
\\\

Pour les étudiants GitHub: Vous pouvez obtenir **LocalStack PRO GRATUIT** avec GitHub Student Pack!

---

### ÉTAPE 8: Démarrer LocalStack

\\\ash
# Lancer LocalStack en arrière-plan
docker run -d --name localstack \
  -p 4566:4566 \
  -p 4571:4571 \
  -e "SERVICES=ec2,vpc" \
  -e "DEBUG=0" \
  -e "LOCALSTACK_AUTH_TOKEN=<votre-token>" \
  localstack/localstack:latest

# Attendre 30-40 secondes pour l'initialisation
# Puis vérifier que c'est prêt
curl http://localhost:4566/_localstack/health
\\\

Résultat attendu:
\\\json
{
  "services": {
    "ec2": "running",
    "vpc": "running"
  },
  "version": "2026.5.0"
}
\\\

**Si ça ne marche pas:** Voir section Dépannage ci-dessous

---

### ÉTAPE 9: Déployer l'Infrastructure

\\\ash
# L'environnement virtuel DOIT être activé
# LocalStack DOIT être en cours d'exécution

# Créer l'infrastructure
python infrastructure/deploy_infrastructure_fixed.py
\\\

Résultat attendu:
\\\
[OK] Infrastructure IDs loaded successfully

=== Creating Infrastructure ===

✓ VPC created: vpc-079e70036f64f1569
✓ Subnet created: subnet-eddce51717da60800
✓ Security Group created: sg-1ef99ff1d5e66b705
✓ Instance 1 created: i-6d99ddefd4746a5c5
✓ Instance 2 created: i-88e6190fe72cba224

✓ Infrastructure created!
\\\

---

### ÉTAPE 10: Lancer le Dashboard

\\\ash
# L'environnement virtuel DOIT être activé
# LocalStack DOIT être en cours d'exécution
# L'infrastructure DOIT être déployée

python flask_dashboard.py
\\\

Résultat attendu:
\\\
======================================================================
 🚀 LOCALSTACK FAILURE SIMULATOR DASHBOARD
======================================================================

📍 Open your browser: http://localhost:5000

Functionality:
  ✓ View all EC2 instances in real-time
  ✓ Monitor instance status (Running/Stopped/Terminated)
  ✓ Control instances (Stop/Start/Terminate)
  ✓ Live metrics and logs

======================================================================

Starting Flask server...

 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
\\\

**Ouvrir dans le navigateur:** http://localhost:5000 ✅

---

## ✅ Vérification de l'Installation

### Checklist Complète

\\\
[ ] Python 3.8+ installé
    python --version

[ ] Docker installé et en cours d'exécution
    docker --version
    docker ps

[ ] Git installé
    git --version

[ ] Projet cloné
    ls infrastructure/
    ls scenarios/

[ ] Environnement virtuel créé et activé
    echo \  (ou echo %VIRTUAL_ENV% sur Windows)

[ ] Dépendances installées
    pip list | grep boto3
    pip list | grep flask

[ ] LocalStack en cours d'exécution
    curl http://localhost:4566/_localstack/health

[ ] Infrastructure déployée
    cat created_ids.json

[ ] Dashboard accessible
    curl http://localhost:5000/
\\\

---

## 🔧 Dépannage

### Problème 1: Docker ne démarre pas

\\\powershell
# Vérifier que Docker Desktop est lancé
docker ps

# Si erreur, redémarrer Docker
# Windows: Redémarrer Docker Desktop depuis le menu Démarrage

# Vérifier les logs
docker logs localstack --tail 50

# Redémarrer le container
docker restart localstack
\\\

---

### Problème 2: LocalStack timeout sur création d'instances

\\\powershell
# C'est NORMAL sur Windows
# Solution: Augmenter le timeout dans le code

# Modifier infrastructure/deploy_infrastructure_fixed.py:
# config = Config(read_timeout=300)  # 5 minutes au lieu de 30 secondes

# Ou vérifier que LocalStack a assez de ressources
# Docker Desktop → Settings → Resources
# Augmenter Memory à 8GB minimum
# Augmenter CPUs à 4+
\\\

---

### Problème 3: Port 4566 déjà utilisé

\\\ash
# Vérifier quel processus utilise le port
# Windows:
netstat -ano | findstr :4566

# macOS/Linux:
lsof -i :4566

# Solution: Arrêter le container existant
docker stop localstack
docker rm localstack

# Ou utiliser un port différent
docker run -d --name localstack \
  -p 4567:4566 \
  ...

# Et modifier ENDPOINT dans les scripts:
# ENDPOINT = "http://localhost:4567"
\\\

---

### Problème 4: Port 5000 déjà utilisé (Flask)

\\\ash
# Vérifier quel processus utilise le port
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Solution 1: Arrêter le processus
# Windows:
taskkill /PID <PID> /F

# Solution 2: Utiliser un autre port
# Modifier flask_dashboard.py:
# app.run(port=5001)

# Puis ouvrir http://localhost:5001
\\\

---

### Problème 5: "ModuleNotFoundError: No module named 'boto3'"

\\\ash
# Vérifier que l'environnement virtuel est activé
# Windows: Vous devez voir (venv) au début de la ligne PowerShell
# macOS/Linux: Vous devez voir (venv) au début

# Si non activé:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Puis réinstaller
pip install -r requirements.txt
\\\

---

### Problème 6: "Connection refused" pour LocalStack

\\\ash
# LocalStack n'est pas en cours d'exécution
# Démarrer LocalStack:
docker run -d --name localstack \
  -p 4566:4566 \
  -e "SERVICES=ec2,vpc" \
  -e "LOCALSTACK_AUTH_TOKEN=<token>" \
  localstack/localstack:latest

# Attendre 30-40 secondes
# Vérifier:
curl http://localhost:4566/_localstack/health

# Vérifier les logs
docker logs localstack
\\\

---

### Problème 7: Erreurs UTF-8/Encoding

\\\ash
# Sur Windows PowerShell, si caractères accentués mal affichés:
# Ajouter au début de chaque script:
# -*- coding: utf-8 -*-

# Ou utiliser:
chcp 65001  # Changer vers UTF-8 dans PowerShell
\\\

---

### Problème 8: "Permission denied" sur macOS/Linux

\\\ash
# Ajouter les permissions d'exécution
chmod +x infrastructure/deploy_infrastructure_fixed.py
chmod +x scenarios/*.py
chmod +x flask_dashboard.py

# Ou exécuter avec python
python infrastructure/deploy_infrastructure_fixed.py
\\\

---

## 🔗 Commandes Utiles

### Gestion Docker

\\\ash
# Démarrer LocalStack
docker run -d --name localstack \
  -p 4566:4566 \
  -e "SERVICES=ec2,vpc" \
  -e "LOCALSTACK_AUTH_TOKEN=<token>" \
  localstack/localstack:latest

# Voir les containers en cours
docker ps

# Voir tous les containers
docker ps -a

# Voir les logs
docker logs -f localstack

# Arrêter le container
docker stop localstack

# Supprimer le container
docker rm localstack

# Nettoyer le système
docker system prune
\\\

---

### Gestion Python

\\\ash
# Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Désactiver l'environnement
deactivate

# Voir les packages installés
pip list

# Mettre à jour pip
pip install --upgrade pip

# Geler les dépendances
pip freeze > requirements.txt

# Installer depuis requirements.txt
pip install -r requirements.txt
\\\

---

### Gestion Git

\\\ash
# Vérifier le statut
git status

# Ajouter les fichiers
git add .

# Commit
git commit -m "Message du commit"

# Pousser sur GitHub
git push origin main

# Voir l'historique
git log --oneline

# Créer une branche
git checkout -b nom-branche

# Changer de branche
git checkout nom-branche
\\\

---

### Exécuter les Scripts

\\\ash
# Déployer l'infrastructure
python infrastructure/deploy_infrastructure_fixed.py

# Contrôle manuel des instances
python scenarios/instance_control.py

# Simuler une panne + recovery
python scenarios/failure_recovery.py

# Monitoring continu
python scenarios/monitoring.py

# Lancer le dashboard
python flask_dashboard.py

# Accéder au dashboard
# Ouvrir dans le navigateur: http://localhost:5000
\\\

---

## 📝 Prochaines Étapes

### Après Installation Réussie

1. **Tester les Scenarios:**
   \\\ash
   python scenarios/failure_recovery.py
   \\\

2. **Explorer le Dashboard:**
   - Ouvrir http://localhost:5000
   - Voir les instances
   - Tester les boutons (Stop, Start, Terminate)

3. **Lancer le Monitoring:**
   \\\ash
   python scenarios/monitoring.py
   \\\

4. **Consulter la Documentation:**
   - Lire README.md
   - Lire ARCHITECTURE.md

5. **Collecter les Données:**
   - Screenshots du dashboard
   - Logs de monitoring
   - Résultats des tests

---

## 📞 Support

Si vous rencontrez des problèmes:

1. **Vérifier les logs:**
   \\\ash
   docker logs localstack
   cat monitoring_log.txt
   \\\

2. **Consulter la FAQ:**
   - Voir section Dépannage ci-dessus
   - Voir README.md

3. **Contacter le responsable infrastructure:**
   - Neriona (Infrastructure et Déploiement)

---

**Dernier mise à jour:** 7 mai 2026  
**Version:** 1.0  
**Statut:** ✅ Complet et Testé
