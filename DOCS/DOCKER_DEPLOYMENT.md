# Déploiement avec Docker

Ce guide explique comment déployer l'application Songon Tour en utilisant Docker et Docker Compose.

## Prérequis

- Docker
- Docker Compose

## Configuration

1. Copiez le fichier d'exemple des variables d'environnement :
   ```bash
   cp .env.example .env
   ```

2. Modifiez le fichier `.env` avec vos valeurs :
   - `SECRET_KEY` : Une clé secrète Django sécurisée
   - `ALLOWED_HOSTS` : Vos domaines autorisés (séparés par des virgules)

## Déploiement

1. Construisez et lancez les conteneurs :
   ```bash
   docker-compose up --build -d
   ```

2. Appliquez les migrations de base de données :
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Collectez les fichiers statiques :
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

4. Créez un superutilisateur (optionnel) :
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Accès

- Application : http://localhost
- Admin Django : http://localhost/admin/

## Commandes utiles

- Arrêter les conteneurs :
  ```bash
  docker-compose down
  ```

- Voir les logs :
  ```bash
  docker-compose logs -f
  ```

- Redémarrer un service :
  ```bash
  docker-compose restart web
  ```

## Production

Pour un déploiement en production :

1. Utilisez un reverse proxy comme Traefik ou un load balancer
2. Configurez HTTPS avec Let's Encrypt
3. Utilisez une base de données PostgreSQL au lieu de SQLite
4. Configurez les variables d'environnement appropriées
5. Utilisez des volumes persistants pour les données

## Structure

- `web` : Service Django avec Gunicorn
- `nginx` : Serveur web pour les fichiers statiques et proxy
- Volumes : `static_volume` et `media_volume` pour la persistance