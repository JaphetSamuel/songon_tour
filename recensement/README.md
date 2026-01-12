# Module de Recensement des Jeunes - Commune de Songon

## Description
Le module de recensement permet d'enregistrer et de gérer les informations des jeunes de la commune de Songon. Il offre une interface web pour créer, visualiser, modifier et supprimer les profils des jeunes enregistrés.

## Fonctionnalités

### 1. Enregistrement des Jeunes
- Formulaire complet pour l'enregistrement des jeunes
- Validation automatique des données
- Attribution d'un matricule unique généré automatiquement

### 2. Gestion des Profils
- **Lister**: Voir tous les jeunes enregistrés avec pagination
- **Créer**: Enregistrer un nouveau jeune
- **Voir les détails**: Consulter les informations complètes d'un jeune
- **Modifier**: Mettre à jour les informations d'un jeune
- **Supprimer**: Supprimer un profil avec confirmation

### 3. Champs du Formulaire

#### Informations Personnelles
- Nom (requis)
- Prénom (requis)
- Âge (requis, entre 16 et 100 ans)
- Genre (Masculin/Féminin)
- Numéro CNI/Passeport (requis, unique)
- Matricule (auto-généré)

#### Adresse et Contact
- Zone de résidence (requis)
- Adresse complète (requis)
- Téléphone principal (requis)
- Téléphone secondaire (optionnel)
- Email (optionnel)

#### Éducation et Compétences
- Niveau d'étude (Primaire, Secondaire, BAC, Licence, Master, Doctorat, Pas de scolarité)
- Domaine d'activité (optionnel)
- Compétences (requis - description des savoir-faire)

## URLs

```
/fr/recensement/jeunes/                    - Liste de tous les jeunes
/fr/recensement/jeunes/nouveau/           - Formulaire pour créer un nouveau jeune
/fr/recensement/jeunes/<id>/              - Détails d'un jeune
/fr/recensement/jeunes/<id>/modifier/     - Formulaire pour modifier un jeune
/fr/recensement/jeunes/<id>/supprimer/    - Confirmation de suppression
```

## Vues (Class-Based Views)

### JeuneCreateView
- Crée un nouveau jeune
- Affiche le formulaire
- Redirige vers la liste après succès

### JeuneListView
- Liste tous les jeunes avec pagination (20 par page)
- Permet la recherche et le filtrage

### JeuneDetailView
- Affiche les détails complets d'un jeune
- Fournit des actions (modifier, supprimer, retour)

### JeuneUpdateView
- Permet de modifier un jeune existant
- Valide les données
- Redirige vers la liste après succès

### JeuneDeleteView
- Demande confirmation avant suppression
- Supprime définitivement le profil
- Redirige vers la liste après succès

## Formulaire Django

**JeuneForm** (ModelForm)
- Basé sur le modèle Jeune
- Validation personnalisée:
  - Vérification de l'unicité du numéro CNI
  - Validation de l'âge (16-100 ans)
- Widgets personnalisés avec Bootstrap
- Messages d'erreur localisés

## Admin Django

L'interface d'administration Django permet de:
- Gérer les jeunes en arrière-plan
- Filtrer par genre, domaine d'activité, niveau d'étude
- Rechercher par nom, prénom, CNI, matricule
- Visualiser les informations dans des sections groupées

## Installation et Configuration

1. **Assurez-vous que l'app est installée dans `INSTALLED_APPS`**:
   ```python
   INSTALLED_APPS = [
       ...
       'recensement',
   ]
   ```

2. **Les migrations doivent être appliquées**:
   ```bash
   python manage.py migrate
   ```

3. **Les URLs doivent être incluses dans le fichier principal urls.py**

## Modèle de Données

```python
class Jeune(models.Model):
    nom = CharField(max_length=100)
    prenom = CharField(max_length=100)
    age = IntegerField()
    genre = CharField(max_length=10)
    zone = CharField(max_length=100)
    adresse = TextField()
    telephone = CharField(max_length=15)
    telephone2 = CharField(max_length=15, blank=True, null=True)
    email = EmailField(blank=True, null=True)
    Domaine_activite = CharField(max_length=100, null=True, blank=True)
    Niveau_etude = CharField(max_length=100, null=True, blank=True)
    competences = TextField()
    numero_cni = CharField(max_length=50, unique=True)
    matricule = CharField(max_length=50, unique=True, null=True, blank=True)
```

## Génération du Matricule

Le matricule est généré automatiquement au format: `J{unique_id}`
- Préfixe: "J"
- ID unique basé sur les 4 derniers chiffres du numéro CNI
- Exemple: J00789 (si le CNI se termine par 789)

## Templates

Tous les templates héritent de `home/layout/base.html` pour un design cohérent:
- `jeune_form.html` - Formulaire pour créer/modifier un jeune
- `jeune_list.html` - Liste de tous les jeunes
- `jeune_detail.html` - Détails d'un jeune
- `jeune_confirm_delete.html` - Confirmation de suppression

## Styles CSS

- Bootstrap 5 pour la mise en page responsive
- Styles personnalisés pour les formulaires
- Responsive design pour mobile et desktop
- Messages de succès et d'erreur intégrés

## Validations

1. **Numéro CNI**:
   - Requis
   - Unique (impossible d'enregistrer deux jeunes avec le même CNI)

2. **Âge**:
   - Entre 16 et 100 ans

3. **Champs requis**:
   - Nom, Prénom, Âge, Genre, Zone, Adresse, Téléphone, Compétences, Numéro CNI

4. **Champs optionnels**:
   - Téléphone 2, Email, Domaine d'activité, Niveau d'étude

## Utilisation

### Pour accéder au formulaire d'enregistrement:
Visitez `/fr/recensement/jeunes/nouveau/`

### Pour voir tous les jeunes enregistrés:
Visitez `/fr/recensement/jeunes/`

### Pour voir le détail d'un jeune:
Visitez `/fr/recensement/jeunes/<id>/`

### Pour modifier un jeune:
Allez sur sa fiche détail et cliquez sur "Modifier"

### Pour supprimer un jeune:
Allez sur sa fiche détail et cliquez sur "Supprimer" (confirmation demandée)

## Notes de Sécurité

- Les formulaires utilisent la protection CSRF de Django
- Les mots de passe ne sont pas stockés (données civiles uniquement)
- L'accès aux vues peut être restreint avec des permissions Django
- Les données sensibles (téléphone, email) sont affichées uniquement aux utilisateurs autorisés
