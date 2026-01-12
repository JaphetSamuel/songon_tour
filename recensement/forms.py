from django import forms
from .models import Jeune


class JeuneForm(forms.ModelForm):
    """Formulaire pour créer et modifier les informations d'un jeune"""
    
    class Meta:
        model = Jeune
        fields = [
            'nom',
            'prenom',
            'age',
            'genre',
            'zone',
            'adresse',
            'telephone',
            'telephone2',
            'email',
            'Domaine_activite',
            'Niveau_etude',
            'competences',
            'numero_cni',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre nom de famille',
                'required': True
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre prénom',
                'required': True
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre âge',
                'min': '16',
                'max': '70',
                'required': True
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control nice-select wide',
                'required': True
            }, choices=[
                ('', 'Sélectionnez votre genre'),
                ('Masculin', 'Masculin'),
                ('Féminin', 'Féminin'),
            ]),
            'zone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre zone de résidence',
                'required': True
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre adresse complète',
                'rows': 3,
                'required': True
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+225 XX XX XX XX',
                'type': 'tel',
                'required': True
            }),
            'telephone2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+225 XX XX XX XX (optionnel)',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@exemple.com',
                'type': 'email'
            }),
            'Domaine_activite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Informatique, Agriculture, Commerce...'
            }),
            'Niveau_etude': forms.Select(attrs={
                'class': 'form-control nice-select wide'
            }, choices=[
                ('', 'Sélectionnez votre niveau d\'étude'),
                ('Primaire', 'Primaire'),
                ('Secondaire', 'Secondaire'),
                ('BAC', 'BAC'),
                ('Licence', 'Licence'),
                ('Master', 'Master'),
                ('Doctorat', 'Doctorat'),
                ('Pas de scolarité', 'Pas de scolarité'),
            ]),
            'competences': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez vos compétences et savoir-faire',
                'rows': 4,
                'required': True
            }),
            'numero_cni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de votre CNI/Passeport',
                'required': True
            }),
        }

    def clean_numero_cni(self):
        numero_cni = self.cleaned_data.get('numero_cni')
        if numero_cni:
            # Vérifier si le numéro CNI existe déjà (sauf en cas de modification)
            if self.instance.pk is None:
                if Jeune.objects.filter(numero_cni=numero_cni).exists():
                    raise forms.ValidationError(
                        "Cette personne est déjà enregistrée dans le système."
                    )
        return numero_cni

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 16 or age > 100):
            raise forms.ValidationError("L'âge doit être entre 16 et 100 ans.")
        return age
