# Guide d'Intégration du Module de Recensement

## 1️⃣ Ajouter le Lien au Menu de Navigation

### Modifier `home/templates/home/layout/header.html`

Trouvez le menu de navigation et ajoutez:

```html
<!-- Récensement des Jeunes -->
<li class="dropdown">
    <a href="{% url 'jeune_list' %}">Recensement</a>
    <ul class="sub-menu">
        <li><a href="{% url 'jeune_list' %}">Voir les jeunes enregistrés</a></li>
        <li><a href="{% url 'jeune_create' %}">Enregistrer un jeune</a></li>
    </ul>
</li>
```

## 2️⃣ Ajouter un Bouton d'Appel à l'Action

### Sur la page d'accueil (home/templates/home/index.html)

Vous pouvez ajouter une section pour promouvoir le récensement:

```html
<section class="cta-section">
    <div class="container">
        <h2>Faites-vous enregistrer!</h2>
        <p>Rejoignez le programme de récensement des jeunes de la commune de Songon.</p>
        <a href="{% url 'jeune_create' %}" class="thm-btn">
            <i class="icon-user-plus"></i> S'enregistrer maintenant
        </a>
    </div>
</section>
```

## 3️⃣ Ajouter un Lien dans le Footer

### Modifier `home/templates/home/layout/base.html` (section footer)

```html
<div class="footer-widget">
    <h3 class="footer-widget__title">Récensement</h3>
    <ul class="footer-list">
        <li><a href="{% url 'jeune_list' %}">Voir les jeunes enregistrés</a></li>
        <li><a href="{% url 'jeune_create' %}">Enregistrer un jeune</a></li>
    </ul>
</div>
```

## 4️⃣ Créer une Page d'Accueil pour le Module

### Créer `recensement/templates/recensement/index.html`

```html
{% extends 'home/layout/base.html' %}
{% load static %}

{% block title %}Récensement des Jeunes{% endblock %}

{% block content %}
<section class="page-title">
    <div class="page-title__bg" style="background-image: url({% static 'assets/images/backgrounds/page-title-bg.jpg' %});"></div>
    <div class="container">
        <div class="row">
            <div class="col-xl-8 col-lg-8">
                <h1 class="page-title__title">Programme de Récensement</h1>
                <p class="page-title__text">
                    Enregistrez-vous et rejoignez la base de données des jeunes de la commune
                </p>
            </div>
        </div>
    </div>
</section>

<section class="about-two">
    <div class="container">
        <div class="row">
            <div class="col-xl-6">
                <h2>Pourquoi s'enregistrer?</h2>
                <ul>
                    <li>Être identifié comme jeune talent de la commune</li>
                    <li>Accéder à des opportunités</li>
                    <li>Partager vos compétences</li>
                    <li>Faire partie de la communauté</li>
                </ul>
                <a href="{% url 'jeune_create' %}" class="thm-btn">
                    S'enregistrer maintenant
                </a>
            </div>
            <div class="col-xl-6">
                <img src="{% static 'assets/images/resources/census.jpg' %}" alt="Récensement" />
            </div>
        </div>
    </div>
</section>

<section class="statistics">
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="stat-card">
                    <h3>{{ total_jeunes }}</h3>
                    <p>Jeunes enregistrés</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <h3>{{ total_jeunes_masculins }}</h3>
                    <p>Jeunes hommes</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <h3>{{ total_jeunes_feminins }}</h3>
                    <p>Jeunes femmes</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <h3>{{ total_domaines }}</h3>
                    <p>Domaines d'activité</p>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}
```

Puis créer la vue correspondante dans `views.py`:

```python
from django.views.generic import TemplateView
from django.db.models import Count, Q

class RecensementIndexView(TemplateView):
    template_name = 'recensement/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_jeunes'] = Jeune.objects.count()
        context['total_jeunes_masculins'] = Jeune.objects.filter(genre='Masculin').count()
        context['total_jeunes_feminins'] = Jeune.objects.filter(genre='Féminin').count()
        context['total_domaines'] = Jeune.objects.values('Domaine_activite').distinct().count()
        return context
```

Et ajouter dans `urls.py`:

```python
from django.views.generic import TemplateView

urlpatterns = [
    # Accueil du module
    path('', RecensementIndexView.as_view(), name='recensement_index'),
    
    # Reste des URLs...
]
```

## 5️⃣ Ajouter une Classe CSS pour les Cartes de Statistiques

Ajouter au `home/static/assets/css/custom.css`:

```css
.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 2rem;
    transition: transform 0.3s;
}

.stat-card:hover {
    transform: translateY(-5px);
}

.stat-card h3 {
    font-size: 2.5rem;
    margin: 0;
    font-weight: 700;
}

.stat-card p {
    margin: 0.5rem 0 0 0;
    font-size: 0.95rem;
    opacity: 0.9;
}
```

## 6️⃣ Ajouter des Permissions (Optionnel)

Pour restreindre l'accès au formulaire d'enregistrement aux utilisateurs authentifiés:

Modifier `views.py`:

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class JeuneCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # ...
    login_url = 'login'  # URL de la page de connexion
```

## 7️⃣ Configuration des E-mails (Optionnel)

Pour envoyer une confirmation par e-mail après l'enregistrement:

```python
from django.core.mail import send_mail
from django.template.loader import render_to_string

class JeuneCreateView(SuccessMessageMixin, CreateView):
    # ...
    
    def form_valid(self, form):
        response = super().form_valid(form)
        jeune = form.instance
        
        # Envoyer un email de confirmation
        if jeune.email:
            subject = f'Confirmation - {jeune.matricule}'
            message = render_to_string('recensement/email_confirmation.html', {
                'jeune': jeune,
            })
            send_mail(subject, message, 'from@example.com', [jeune.email])
        
        return response
```

## 8️⃣ Créer une Page de Gestion (Optionnel)

Pour les administrateurs qui veulent une vue d'ensemble:

```python
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

@method_decorator(staff_member_required, name='dispatch')
class JeuneStatsView(TemplateView):
    template_name = 'recensement/stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_jeunes'] = Jeune.objects.count()
        context['jeunes_par_genre'] = Jeune.objects.values('genre').annotate(
            count=Count('id')
        )
        context['jeunes_par_domaine'] = Jeune.objects.values('Domaine_activite').annotate(
            count=Count('id')
        )
        return context
```

## 9️⃣ Intégration avec les Tâches Planifiées (Celery)

Si vous utilisez Celery pour les tâches asynchrones:

```python
from celery import shared_task

@shared_task
def envoi_rappel_inscription():
    """Envoie un rappel aux jeunes non enregistrés"""
    jeunes = Jeune.objects.all()
    for jeune in jeunes:
        if jeune.email:
            send_mail(
                'Mettez à jour votre profil',
                'Cliquez ici pour mettre à jour...',
                'from@example.com',
                [jeune.email]
            )
```

## 🔟 Checklist d'Intégration

- [ ] Ajouter le lien au menu principal
- [ ] Ajouter un CTA sur la page d'accueil
- [ ] Ajouter un lien dans le footer
- [ ] Tester tous les liens
- [ ] Ajouter les images appropriées
- [ ] Configurer les e-mails (optionnel)
- [ ] Ajouter les permissions (optionnel)
- [ ] Tester sur mobile et desktop
- [ ] Former l'équipe à l'utilisation
- [ ] Lancer la campagne de communication

## URL Complètes (avec i18n)

```
https://votresite.com/fr/recensement/              - Accueil module
https://votresite.com/fr/recensement/jeunes/       - Liste des jeunes
https://votresite.com/fr/recensement/jeunes/nouveau/ - Formulaire
https://votresite.com/fr/recensement/jeunes/1/     - Détails
https://votresite.com/fr/admin/                    - Admin Django
```
