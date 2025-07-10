# Location Sociale – Backend Django
###  Prérequis
- Python 3.9 ou plus
- pip
- Git
- Node.js et npm (pour le frontend)
- SQLite (déjà intégré à Python)

-----------------------------------
1. **Cloner le dépôt**
```bash
git clone https://github.com/azertykane/Django-vuejs.git
# 2. Créer un environnement virtuel
python -m venv venv
# (Windows) venv\Scripts\activate
# (Unix/macOS) source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Copier le fichier d'exemple d'environnement
cp .env.example .env
# Remplir les valeurs dans le fichier `.env`

# 5. Appliquer les migrations
cd backend
python manage.py migrate

# 6. Lancer le serveur local
python manage.py runserver