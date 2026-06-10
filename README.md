# ExpenseAI — Tactical Command Center

Application web de traitement automatisé de notes de frais, alimentée par l'IA.

## Fonctionnement

1. L'utilisateur uploade une photo de justificatif (ticket, facture, reçu)
2. Le modèle de vision IA (Llama 4 via Groq) extrait les données automatiquement
3. Un formulaire pré-rempli apparaît pour vérification et correction
4. La ligne est enregistrée dans un Google Sheet

## Stack technique

- **Backend** : Python, FastAPI, Uvicorn
- **IA** : Groq API — `meta-llama/llama-4-scout-17b-16e-instruct`
- **Google** : gspread, Google Sheets API, Google Drive API
- **Frontend** : HTML, CSS, JS vanilla, HTMX

## Structure

```
expense-tracker/
├── app.py              # Serveur FastAPI (routes GET /, POST /api/analyze, POST /api/submit)
├── backend.py          # Classe ExpenseAgent — extraction IA depuis image
├── sheets.py           # Classe GoogleSheetsClient — Sheets + Drive
├── context.txt         # Prompt système de l'agent IA
├── prompt.txt          # Prompt utilisateur + schéma JSON attendu
├── requirements.txt    # Dépendances Python
├── .env.example        # Template des variables d'environnement
└── static/
    ├── index.html      # Interface principale (HTMX)
    ├── style.css       # Thème Valorant dark
    └── app.js          # Prévisualisation image + drag & drop
```

## Installation

```bash
# 1. Cloner le repo et aller dans le dossier
cd expense-tracker

# 2. Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Remplir les valeurs dans .env
```

## Configuration `.env`

```env
GROQ_API_KEY=""                    # Clé API Groq
GOOGLE_SHEET_ID=""                 # ID du Google Sheet
GOOGLE_SERVICE_ACCOUNT_JSON=""     # Chemin vers la clé JSON du compte de service
GOOGLE_DRIVE_FOLDER_ID=""          # ID du dossier Drive pour les images (optionnel)
```

## Prérequis Google

- Activer **Google Sheets API** et **Google Drive API** dans Google Cloud Console
- Créer un compte de service et télécharger la clé JSON
- Partager le Google Sheet avec l'email du compte de service (rôle Éditeur)
- La feuille doit s'appeler **"Notes de frais"**

## Lancer l'application

```bash
uvicorn app:app --reload
```

Ouvrir **http://localhost:8000**

## Arrêter l'application

```bash
pkill -f "uvicorn app:app"
```
