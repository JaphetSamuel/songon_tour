# Exemples d'Utilisation du Module de Recensement

## 1. Création d'un Jeune via le Shell Django

```python
python manage.py shell
```

```python
from recensement.models import Jeune

# Créer un jeune
jeune = Jeune.objects.create(
    nom='Dupont',
    prenom='Jean',
    age=25,
    genre='Masculin',
    zone='Zone Centre',
    adresse='123 Rue de la Liberté, Songon',
    telephone='+225 07 12 34 56 78',
    telephone2='+225 01 98 76 54 32',
    email='jean.dupont@example.com',
    Domaine_activite='Informatique',
    Niveau_etude='Licence',
    competences='Python, Django, JavaScript, Gestion de projet',
    numero_cni='CI123456789'
)

# Afficher le jeune créé
print(jeune)  # Dupont Jean
print(jeune.matricule)  # J00789 (auto-généré)
```

## 2. Récupérer et Filtrer les Jeunes

```python
from recensement.models import Jeune

# Tous les jeunes
tous_les_jeunes = Jeune.objects.all()

# Jeunes par genre
jeunes_masculins = Jeune.objects.filter(genre='Masculin')
jeunes_feminins = Jeune.objects.filter(genre='Féminin')

# Jeunes par zone
jeunes_zone_centre = Jeune.objects.filter(zone='Zone Centre')

# Jeunes avec un domaine spécifique
jeunes_informatique = Jeune.objects.filter(Domaine_activite='Informatique')

# Jeunes avec un niveau d'étude
jeunes_licence = Jeune.objects.filter(Niveau_etude='Licence')

# Combinaisons
jeunes_jeunes_hommes_informaticiens = Jeune.objects.filter(
    genre='Masculin',
    Domaine_activite='Informatique',
    age__gte=18  # Age >= 18
)

# Tri
jeunes_tries_par_age = Jeune.objects.all().order_by('age')
jeunes_recents = Jeune.objects.all().order_by('-id')
```

## 3. Statistiques

```python
from django.db.models import Count, Q, Avg, Min, Max
from recensement.models import Jeune

# Nombre total de jeunes
total = Jeune.objects.count()

# Nombre de jeunes par genre
par_genre = Jeune.objects.values('genre').annotate(count=Count('id'))
# Output: <QuerySet [{'genre': 'Masculin', 'count': 15}, ...]>

# Nombre de jeunes par domaine
par_domaine = Jeune.objects.values('Domaine_activite').annotate(
    count=Count('id')
).order_by('-count')

# Nombre de jeunes par zone
par_zone = Jeune.objects.values('zone').annotate(
    count=Count('id')
).order_by('-count')

# Âge moyen
age_moyen = Jeune.objects.aggregate(Avg('age'))['age__avg']

# Âge minimum et maximum
ages = Jeune.objects.aggregate(
    min_age=Min('age'),
    max_age=Max('age')
)

# Jeunes avec email
avec_email = Jeune.objects.exclude(email__isnull=True).exclude(email__exact='').count()

# Recherche par texte
resultats = Jeune.objects.filter(
    Q(nom__icontains='dupont') |
    Q(prenom__icontains='jean') |
    Q(email__icontains='example')
)
```

## 4. Modification et Suppression

```python
from recensement.models import Jeune

# Modifier un jeune
jeune = Jeune.objects.get(id=1)
jeune.age = 26
jeune.email = 'newemail@example.com'
jeune.save()

# Modifier plusieurs jeunes
Jeune.objects.filter(zone='Zone Centre').update(
    zone='Zone Songon Centre'
)

# Supprimer un jeune
jeune = Jeune.objects.get(id=1)
jeune.delete()

# Supprimer plusieurs jeunes
Jeune.objects.filter(zone='Old Zone').delete()
```

## 5. Recherche Avancée

```python
from django.db.models import Q
from recensement.models import Jeune

# Jeunes entre deux âges
jeunes_20_30 = Jeune.objects.filter(age__gte=20, age__lte=30)

# Jeunes né après une certaine date
jeunes_recents = Jeune.objects.all().order_by('-id')[:10]

# Recherche par numéro CNI
jeune = Jeune.objects.get(numero_cni='CI123456789')

# Jeunes sans email renseigné
sans_email = Jeune.objects.filter(email__isnull=True) | \
             Jeune.objects.filter(email__exact='')

# Jeunes avec téléphone secondaire
avec_tel2 = Jeune.objects.exclude(telephone2__isnull=True).exclude(telephone2__exact='')
```

## 6. Import en Masse (Bulk Operations)

```python
from recensement.models import Jeune

# Créer plusieurs jeunes à la fois
jeunes = [
    Jeune(
        nom='Martin',
        prenom='Paul',
        age=28,
        genre='Masculin',
        zone='Zone 1',
        adresse='Rue A',
        telephone='+225 07 XX XX XX XX',
        competences='Commerce',
        numero_cni='CI111111111'
    ),
    Jeune(
        nom='Martin',
        prenom='Marie',
        age=25,
        genre='Féminin',
        zone='Zone 2',
        adresse='Rue B',
        telephone='+225 07 XX XX XX XX',
        competences='Éducation',
        numero_cni='CI222222222'
    ),
]

Jeune.objects.bulk_create(jeunes)
```

## 7. Export de Données

```python
import csv
from django.http import HttpResponse
from recensement.models import Jeune

def export_jeunes_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jeunes.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Matricule', 'Nom', 'Prénom', 'Âge', 'Genre', 
        'Zone', 'Téléphone', 'Email', 'Domaine'
    ])
    
    for jeune in Jeune.objects.all():
        writer.writerow([
            jeune.matricule,
            jeune.nom,
            jeune.prenom,
            jeune.age,
            jeune.genre,
            jeune.zone,
            jeune.telephone,
            jeune.email,
            jeune.Domaine_activite,
        ])
    
    return response
```

## 8. Signal Django (Actions Automatiques)

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from recensement.models import Jeune

@receiver(post_save, sender=Jeune)
def jeune_created(sender, instance, created, **kwargs):
    """Envoyer un email de bienvenue après création"""
    if created and instance.email:
        send_mail(
            'Bienvenue dans le programme de récensement!',
            f'Bonjour {instance.prenom},\n\nVous avez été enregistré avec le matricule: {instance.matricule}',
            'no-reply@songon.com',
            [instance.email],
        )

@receiver(post_delete, sender=Jeune)
def jeune_deleted(sender, instance, **kwargs):
    """Envoyer une notification de suppression"""
    print(f"Le jeune {instance.prenom} {instance.nom} a été supprimé")
```

## 9. Authentification et Permissions

```python
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from recensement.models import Jeune

# Créer un groupe pour les gestionnaires du récensement
group, created = Group.objects.get_or_create(name='Gestionnaires Récensement')

# Ajouter des permissions
content_type = ContentType.objects.get_for_model(Jeune)
permissions = Permission.objects.filter(
    codename__in=['add_jeune', 'change_jeune', 'delete_jeune', 'view_jeune'],
    content_type=content_type,
)
group.permissions.set(permissions)

# Ajouter un utilisateur au groupe
user = User.objects.get(username='admin')
user.groups.add(group)
```

## 10. Utilisation dans les Templates

```html
<!-- Liste tous les jeunes -->
{% for jeune in jeunes %}
    <div class="jeune-card">
        <h3>{{ jeune.prenom }} {{ jeune.nom }}</h3>
        <p>Âge: {{ jeune.age }} ans</p>
        <p>Zone: {{ jeune.zone }}</p>
        <p>Matricule: {{ jeune.matricule }}</p>
        <a href="{% url 'jeune_detail' jeune.pk %}">Voir détails</a>
    </div>
{% endfor %}

<!-- Vérifier si un jeune existe -->
{% if jeune %}
    <p>{{ jeune.prenom }} {{ jeune.nom }} est enregistré</p>
{% else %}
    <p>Aucun jeune trouvé</p>
{% endif %}

<!-- Afficher les messages -->
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

## 11. Requêtes API (Si vous ajoutez Django REST Framework)

```python
# views.py
from rest_framework import viewsets
from .models import Jeune
from .serializers import JeuneSerializer

class JeuneViewSet(viewsets.ModelViewSet):
    queryset = Jeune.objects.all()
    serializer_class = JeuneSerializer

# urls.py
from rest_framework.routers import DefaultRouter
from .views import JeuneViewSet

router = DefaultRouter()
router.register(r'jeunes', JeuneViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

# Utilisation
GET    /api/jeunes/                    # Liste
POST   /api/jeunes/                    # Créer
GET    /api/jeunes/1/                  # Détail
PUT    /api/jeunes/1/                  # Modifier
DELETE /api/jeunes/1/                  # Supprimer
```

## 12. Tests Unitaires Complets

```python
from django.test import TestCase, Client
from django.urls import reverse
from .models import Jeune

class JeuneTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.jeune = Jeune.objects.create(
            nom='Test',
            prenom='User',
            age=25,
            genre='Masculin',
            zone='Zone Test',
            adresse='Test Address',
            telephone='+225 00 00 00 00 00',
            competences='Test',
            numero_cni='CI999999999'
        )
    
    def test_jeune_creation(self):
        self.assertEqual(Jeune.objects.count(), 1)
        self.assertEqual(self.jeune.nom, 'Test')
    
    def test_jeune_list_view(self):
        response = self.client.get(reverse('jeune_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_jeune_detail_view(self):
        response = self.client.get(reverse('jeune_detail', args=[self.jeune.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.jeune.nom)
    
    def test_jeune_create_view(self):
        response = self.client.post(reverse('jeune_create'), {
            'nom': 'Nouveau',
            'prenom': 'Jeune',
            'age': 30,
            'genre': 'Féminin',
            'zone': 'Zone Nouvelle',
            'adresse': 'Nouvelle Adresse',
            'telephone': '+225 11 11 11 11 11',
            'competences': 'Nouvelle Compétence',
            'numero_cni': 'CI888888888'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertEqual(Jeune.objects.count(), 2)
```

## 13. Génération de Rapports

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from django.http import HttpResponse
from .models import Jeune

def generate_rapport(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_jeunes.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Ajouter un titre
    title = Paragraph("<b>Rapport - Jeunes Enregistrés</b>", style=ParagraphStyle(fontSize=16))
    elements.append(title)
    elements.append(Spacer(1, 0.5*inch))
    
    # Ajouter les données
    data = [['Nom', 'Prénom', 'Âge', 'Domaine']]
    for jeune in Jeune.objects.all():
        data.append([jeune.nom, jeune.prenom, jeune.age, jeune.Domaine_activite])
    
    table = Table(data)
    elements.append(table)
    
    doc.build(elements)
    return response
```

Ces exemples couvrent la plupart des cas d'usage courants du module de récensement!
