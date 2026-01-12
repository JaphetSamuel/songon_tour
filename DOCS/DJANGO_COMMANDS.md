# 🛠️ Commandes Django Utiles pour le Module de Recensement

## 🚀 Commandes de Démarrage

### Initialisation du Module

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur pour l'admin
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver

# Lancer sur un port spécifique
python manage.py runserver 0.0.0.0:8000
```

## 🧪 Commandes de Test

```bash
# Exécuter tous les tests
python manage.py test

# Exécuter les tests du module de recensement
python manage.py test recensement

# Exécuter un test spécifique
python manage.py test recensement.tests.JeuneModelTest

# Exécuter un test spécifique avec verbosité
python manage.py test recensement.tests.JeuneModelTest.test_jeune_creation -v 2

# Exécuter avec couverture de code
coverage run --source='.' manage.py test
coverage report
coverage html

# Exécuter avec pdb (debugger)
python manage.py test --pdb
```

## 📊 Commandes de Gestion des Données

### Shell Django

```bash
# Ouvrir le shell Django
python manage.py shell

# Ouvrir le shell avec IPython (si installé)
python manage.py shell_plus
```

### Exemples dans le Shell

```python
# Importer le modèle
from recensement.models import Jeune

# Voir le nombre total de jeunes
Jeune.objects.count()

# Voir tous les jeunes
for jeune in Jeune.objects.all():
    print(jeune)

# Créer un jeune
Jeune.objects.create(
    nom='Test',
    prenom='User',
    age=25,
    genre='Masculin',
    zone='Zone Test',
    adresse='Test',
    telephone='+225 00 00 00 00 00',
    competences='Test',
    numero_cni='CI000000000'
)

# Supprimer tous les jeunes de test
Jeune.objects.filter(nom='Test').delete()

# Quitter
exit()
```

## 📁 Commandes de Gestion des Fichiers

```bash
# Collecter les fichiers statiques
python manage.py collectstatic

# Nettoyer les fichiers statiques
python manage.py clearsessions

# Créer un fichier de données de fixture
python manage.py dumpdata recensement > fixtures/recensement.json

# Charger des données de fixture
python manage.py loaddata fixtures/recensement.json
```

## 🔍 Commandes de Diagnostic

```bash
# Vérifier l'intégrité du projet
python manage.py check

# Vérifier les migrations en attente
python manage.py showmigrations

# Voir les routes disponibles
python manage.py show_urls

# Voir la structure SQL des modèles
python manage.py sqlmigrate recensement 0001

# Voir le SQL généré pour une requête ORM
python manage.py dbshell
```

## 📝 Commandes de Migration

```bash
# Voir l'état des migrations
python manage.py showmigrations

# Créer une nouvelle migration
python manage.py makemigrations

# Créer une migration vide (pour des opérations personnalisées)
python manage.py makemigrations --empty recensement --name custom_name

# Appliquer les migrations
python manage.py migrate

# Appliquer jusqu'à une migration spécifique
python manage.py migrate recensement 0001

# Revenir en arrière (annuler une migration)
python manage.py migrate recensement 0000

# Montrer le SQL qui sera exécuté
python manage.py migrate --plan
```

## 🛡️ Commandes de Sécurité

```bash
# Vérifier les problèmes de sécurité
python manage.py check --deploy

# Générer une nouvelle clé secrète
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())

# Tester les permissions
python manage.py test --keepdb
```

## 📊 Commandes d'Administration

```bash
# Créer un utilisateur
python manage.py createsuperuser

# Créer un utilisateur en batch
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('admin', 'admin@example.com', 'password')

# Changer le mot de passe d'un utilisateur
python manage.py changepassword username

# Supprimer un utilisateur
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.get(username='username').delete()
```

## 🧹 Commandes de Nettoyage

```bash
# Supprimer les fichiers temporaires
python manage.py clearsessions

# Vider le cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Réinitialiser les migrations
python manage.py migrate --fake-initial

# Supprimer la base de données et recommencer
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 🎯 Commandes de Production

```bash
# Collecter les fichiers statiques en production
python manage.py collectstatic --noinput

# Vérifier la configuration de production
python manage.py check --deploy

# Sauvegarder la base de données
python manage.py dumpdata > backup.json

# Restaurer la base de données
python manage.py loaddata backup.json

# Optimiser la base de données
python manage.py dbshell
> VACUUM;  # Pour SQLite
> ANALYZE; # Pour PostgreSQL
```

## 🐛 Commandes de Débogage

```bash
# Lancer le serveur avec debugging
python manage.py runserver --debugger=pdb

# Afficher les requêtes SQL
python manage.py shell
>>> from django.db import connection
>>> from django.test.utils import CaptureQueriesContext
>>> with CaptureQueriesContext(connection) as context:
...     # Votre code ici
>>> print(context.captured_queries)

# Profiler le code
python -m cProfile -s cumtime manage.py runserver

# Tracer les appels
python -c "
import sys
import trace
tracer = trace.Trace(count=False, trace=True)
sys.argv = ['manage.py', 'runserver']
tracer.run('from django.core.management import execute_from_command_line')
"
```

## 📚 Commandes Documentaires

```bash
# Générer la documentation
python manage.py help

# Aide sur une commande spécifique
python manage.py help migrate

# Lister toutes les commandes
python manage.py help --commands

# Voir les modèles disponibles
python manage.py graph_models reviewnsement > models.png
```

## 🔧 Commandes Personnalisées (À Créer)

### Créer une commande personnalisée

```bash
# Créer la structure
mkdir -p recensement/management/commands
touch recensement/management/__init__.py
touch recensement/management/commands/__init__.py
```

### Créer un fichier `export_jeunes.py`:

```python
# recensement/management/commands/export_jeunes.py
from django.core.management.base import BaseCommand
from recensement.models import Jeune
import csv

class Command(BaseCommand):
    help = 'Exporte tous les jeunes en CSV'
    
    def add_arguments(self, parser):
        parser.add_argument('output', type=str, help='Fichier de sortie')
    
    def handle(self, *args, **options):
        with open(options['output'], 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Matricule', 'Nom', 'Prénom', 'Âge', 'Genre'])
            
            for jeune in Jeune.objects.all():
                writer.writerow([
                    jeune.matricule,
                    jeune.nom,
                    jeune.prenom,
                    jeune.age,
                    jeune.genre,
                ])
        
        self.stdout.write(self.style.SUCCESS(
            f"Données exportées dans {options['output']}"
        ))
```

### Utiliser la commande:

```bash
python manage.py export_jeunes output.csv
```

## 📋 Commandes Utiles pour le Développement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Geler les dépendances
pip freeze > requirements.txt

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Formater le code
black .

# Vérifier la qualité du code
flake8 .
pylint .
isort .

# Vérifier les types
mypy .
```

## 🎓 Ressources Utiles

```bash
# Documentation Django
https://docs.djangoproject.com/

# Documentation du modèle
python manage.py help makemigrations

# Tutoriels en ligne
# - Real Python
# - Django for Beginners
# - Two Scoops of Django
```

## 💡 Astuces Productivité

```bash
# Alias pour commandes fréquentes
alias dmr='python manage.py runserver'
alias dms='python manage.py shell'
alias dmt='python manage.py test'
alias dmm='python manage.py migrate'
alias dmmk='python manage.py makemigrations'

# Script de démarrage complet
#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
```

---

**Bonne chance avec votre développement Django!** 🚀
