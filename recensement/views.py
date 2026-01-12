from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Jeune
from .forms import JeuneForm


class JeuneCreateView(SuccessMessageMixin, CreateView):
    """Vue pour créer un nouveau jeune et son compte utilisateur"""
    model = Jeune
    form_class = JeuneForm
    template_name = 'recensement/jeune_form.html'
    success_message = "Le jeune a été enregistré avec succès!"
    
    def get_success_url(self):
        return reverse_lazy('jeune_success', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        # Sauvegarder le jeune d'abord
        response = super().form_valid(form)
        jeune = self.object
        
        # Créer un compte utilisateur automatiquement
        try:
            username = jeune.matricule
            password = jeune.matricule
            
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=jeune.prenom,
                last_name=jeune.nom,
                email=jeune.email if jeune.email else ''
            )
            
            # Envoyer les identifiants par email (simulation)
            self.envoyer_identifiants(jeune, username, password)
            
        except Exception as e:
            print(f"Erreur lors de la création du compte: {e}")
        
        return response
    
    def envoyer_identifiants(self, jeune, username, password):
        """Simuler l'envoi des identifiants par email"""
        if jeune.email:
            # Simuler l'envoi d'email
            sujet = f"Vos identifiants Songon - {jeune.matricule}"
            
            contexte = {
                'prenom': jeune.prenom,
                'nom': jeune.nom,
                'matricule': jeune.matricule,
                'username': username,
                'password': password,
                'email': jeune.email
            }
            
            # Template email
            message_html = render_to_string('recensement/email_credentials.html', contexte)
            message_texte = strip_tags(message_html)
            
            # Afficher dans la console (simulation)
            print(f"\n{'='*60}")
            print(f"📧 EMAIL SIMULATION")
            print(f"{'='*60}")
            print(f"To: {jeune.email}")
            print(f"Subject: {sujet}")
            print(f"{'-'*60}")
            print(message_texte)
            print(f"{'='*60}\n")
            
            # Optionnel: envoyer réellement si configuré
            try:
                send_mail(
                    sujet,
                    message_texte,
                    'no-reply@songon.com',
                    [jeune.email],
                    html_message=message_html,
                    fail_silently=True
                )
            except:
                pass


class JeuneListView(ListView):
    """Vue pour lister tous les jeunes"""
    model = Jeune
    template_name = 'recensement/jeune_list.html'
    context_object_name = 'jeunes'
    paginate_by = 20


class JeuneDetailView(DetailView):
    """Vue pour voir les détails d'un jeune"""
    model = Jeune
    template_name = 'recensement/jeune_detail.html'
    context_object_name = 'jeune'


class JeuneUpdateView(SuccessMessageMixin, UpdateView):
    """Vue pour modifier les informations d'un jeune"""
    model = Jeune
    form_class = JeuneForm
    template_name = 'recensement/jeune_form.html'
    success_url = reverse_lazy('jeune_list')
    success_message = "Les informations ont été mises à jour avec succès!"


class JeuneDeleteView(SuccessMessageMixin, DeleteView):
    """Vue pour supprimer un jeune"""
    model = Jeune
    template_name = 'recensement/jeune_confirm_delete.html'
    success_url = reverse_lazy('jeune_list')
    success_message = "Le jeune a été supprimé avec succès!"


class JeuneSuccessView(DetailView):
    """Vue de succès après l'enregistrement d'un jeune"""
    model = Jeune
    template_name = 'recensement/jeune_success.html'
    context_object_name = 'jeune'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jeune = self.object
        context['prenom'] = jeune.prenom
        context['nom'] = jeune.nom
        context['matricule'] = jeune.matricule
        context['username'] = jeune.matricule
        context['password'] = jeune.matricule
        return context
