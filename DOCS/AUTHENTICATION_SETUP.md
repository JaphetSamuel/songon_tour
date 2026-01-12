# 🔐 AUTHENTIFICATION ET CRÉATION DE COMPTE

## ✨ Nouvelle Fonctionnalité

Après l'enregistrement d'un jeune, un compte utilisateur est **créé automatiquement** avec:
- **Username**: le matricule du jeune
- **Password**: le matricule du jeune

L'utilisateur reçoit:
1. ✅ Une page de succès affichant ses identifiants
2. ✅ Une simulation d'email avec ses identifiants
3. ✅ Redirection vers la page de connexion

Après connexion:
- ✅ Redirection vers la page d'accueil

---

## 📋 Flux d'Utilisation

### 1. Enregistrement
```
Formulaire de Recensement
        ↓
Créer Jeune + Compte Utilisateur
        ↓
Page de Succès (afficher identifiants)
        ↓
Bouton "Se Connecter"
        ↓
Page de Login
```

### 2. Connexion
```
Page de Login
        ↓
Entrer Username (matricule)
        ↓
Entrer Password (matricule)
        ↓
Connexion Réussie
        ↓
Redirection vers Accueil (/)
```

---

## 🔧 Configuration Technique

### Settings.py
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'  # Page d'accueil
```

### Views.py
```python
class JeuneCreateView:
    # Crée automatiquement un User avec:
    # - username = matricule
    # - password = matricule
    # - email = email du jeune
    
class JeuneSuccessView:
    # Affiche la page de succès avec les identifiants
```

### Identifiants par Défaut
- Username: `matricule`
- Password: `matricule`
- Exemple: Username `J00789`, Password `J00789`

---

## 📧 Email de Confirmation

### Contenu
L'email simulé contient:
- Matricule du jeune
- Nom d'utilisateur
- Mot de passe temporaire
- Avertissement de sécurité
- Instructions

### Simulation
L'email est **simulé** (affiché dans la console) et peut être:
- Activé réellement en configurer `EMAIL_BACKEND`
- Modifié avec un template personnalisé

### Activation Réelle d'Email
Pour activer les vrais emails, modifiez `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # ou votre serveur
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'no-reply@songon.com'
```

---

## 🎯 Page de Succès

### URL
```
/fr/recensement/jeunes/<id>/success/
```

### Affichage
- ✅ Matricule (copiable)
- ✅ Nom d'utilisateur (copiable)
- ✅ Mot de passe (masquable, copiable)
- ✅ Avertissements de sécurité
- ✅ Boutons d'action

### Fonctionnalités
1. **Copier au presse-papiers**: Boutons "Copier" pour chaque identifiant
2. **Afficher/Masquer**: Toggle pour masquer le mot de passe
3. **Navigation**: Boutons "Se Connecter" et "Accueil"

---

## 🔒 Sécurité

### Points Forts
1. ✅ Mot de passe temporaire (même que username)
2. ✅ L'utilisateur doit changer son mot de passe après première connexion
3. ✅ Email confirmé uniquement si fourni lors de l'enregistrement
4. ✅ Protection CSRF sur tous les formulaires
5. ✅ Hachage sécurisé du mot de passe

### Avertissements Affichés
- Ne pas partager les identifiants
- Changer le mot de passe après première connexion
- Contacter l'admin en cas d'oubli

---

## 🧪 Test

### Scénario de Test 1: Enregistrement Simple
1. Remplir le formulaire de recensement
2. Soumettre
3. Vérifier:
   - Page de succès affichée
   - Identifiants visibles
   - Email simulé en console
4. Cliquer "Se Connecter"
5. Se connecter avec les identifiants
6. Vérifier redirection vers accueil

### Scénario de Test 2: Sans Email
1. Laisser le champ email vide
2. Soumettre
3. Vérifier:
   - Page de succès affichée
   - Pas d'erreur (email optionnel)
   - Identifiants toujours visibles

### Scénario de Test 3: Doublon de Username
1. Créer un jeune
2. Essayer de créer un autre avec même numéro CNI
3. Vérifier: Erreur sur l'unicité du CNI (avant création de compte)

---

## 🔄 Flux de Données

```
Formulaire Jeune
    ↓
Validation JeuneForm
    ↓
Jeune.objects.create()
    ↓
Générer Matricule (auto)
    ↓
User.objects.create_user(
    username=matricule,
    password=matricule,
    email=jeune.email
)
    ↓
Envoyer Email (simulation)
    ↓
Redirection JeuneSuccessView
    ↓
Afficher Identifiants
    ↓
Redirection Login
    ↓
Afficher Page de Connexion
    ↓
POST Username + Password
    ↓
Authentification
    ↓
Redirection LOGIN_REDIRECT_URL (/)
```

---

## 📌 Points À Retenir

1. **Username = Matricule**: Le username est le matricule généré automatiquement
2. **Password = Matricule**: Le mot de passe initial est identique au username
3. **Redirection**: Après connexion → page d'accueil
4. **Email Optionnel**: Ne pas requis pour créer le compte
5. **Simulation**: Les emails sont affichés dans la console

---

## ✅ Checklist d'Implémentation

- ✅ Vue JeuneCreateView crée le User automatiquement
- ✅ Vue JeuneSuccessView affiche les identifiants
- ✅ Template jeune_success.html créé
- ✅ Email template créé (email_credentials.html)
- ✅ URL `/jeunes/<id>/success/` configurée
- ✅ LOGIN_REDIRECT_URL configuré (vers accueil)
- ✅ Email simulé en console
- ✅ Boutons "Copier" fonctionnels
- ✅ Toggle mot de passe fonctionnel
- ✅ Responsive design

---

## 🚀 Utilisation

### Pour l'Utilisateur
1. Remplir le formulaire d'enregistrement
2. Valider
3. Voir la page de succès avec identifiants
4. Copier les identifiants
5. Cliquer "Se Connecter"
6. Entrer les identifiants
7. Être redirigé vers l'accueil

### Pour l'Administrateur
1. Voir dans la console la simulation d'email envoyé
2. Activer les vrais emails si souhaité
3. Gérer les utilisateurs dans l'admin Django
4. Réinitialiser les mots de passe si oubliés

---

## 🔐 Commandes Utiles

### En Shell Django
```python
# Voir les utilisateurs créés
from django.contrib.auth.models import User
User.objects.all()

# Réinitialiser un mot de passe
user = User.objects.get(username='J00789')
user.set_password('nouveau_password')
user.save()

# Supprimer un utilisateur
user.delete()
```

### En Ligne de Commande
```bash
# Créer un superutilisateur
python manage.py createsuperuser

# Changer le mot de passe d'un user
python manage.py changepassword J00789
```

---

## 📞 FAQ

**Q: Et si je veux changer le mot de passe par défaut?**
R: Modifiez `views.py`, dans `JeuneCreateView.form_valid()`:
```python
password = generate_random_password()  # au lieu de matricule
```

**Q: Comment envoyer les vrais emails?**
R: Configurez `EMAIL_BACKEND` dans `settings.py`

**Q: Que faire si le mot de passe est oublié?**
R: Utiliser `python manage.py changepassword` ou l'admin

**Q: Puis-je changer le username?**
R: Non, c'est le matricule. Changez le matricule dans `models.py`

**Q: Puis-je désactiver la création de compte?**
R: Commentez le `User.objects.create_user()` dans `views.py`

---

## 🎨 Personnalisation

### Modifier les Identifiants
Fichier: `views.py`, méthode `form_valid()`
```python
username = jeune.matricule
password = 'password123'  # Changer ici
```

### Modifier le Email Template
Fichier: `templates/recensement/email_credentials.html`

### Modifier la Page de Succès
Fichier: `templates/recensement/jeune_success.html`

### Modifier la Redirection Après Login
Fichier: `settings.py`
```python
LOGIN_REDIRECT_URL = '/autre-page/'
```

---

**Authentification et Création de Compte: Implémentée! ✅**
