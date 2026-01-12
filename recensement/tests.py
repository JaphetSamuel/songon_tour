from django.test import TestCase, Client
from django.urls import reverse
from .models import Jeune
from .forms import JeuneForm


class JeuneModelTest(TestCase):
    """Tests pour le modèle Jeune"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.jeune = Jeune.objects.create(
            nom='Dupont',
            prenom='Jean',
            age=25,
            genre='Masculin',
            zone='Zone 1',
            adresse='123 Rue de la Paix',
            telephone='+225123456789',
            competences='Informatique, Gestion',
            numero_cni='CI123456789'
        )
    
    def test_jeune_creation(self):
        """Test la création d'un jeune"""
        self.assertEqual(self.jeune.nom, 'Dupont')
        self.assertEqual(self.jeune.prenom, 'Jean')
        self.assertTrue(self.jeune.matricule)
    
    def test_jeune_str(self):
        """Test la représentation string du jeune"""
        self.assertEqual(str(self.jeune), 'Dupont Jean')
    
    def test_matricule_generation(self):
        """Test la génération automatique du matricule"""
        self.assertIsNotNone(self.jeune.matricule)
        self.assertTrue(self.jeune.matricule.startswith('J'))


class JeuneFormTest(TestCase):
    """Tests pour le formulaire Jeune"""
    
    def test_valid_form(self):
        """Test un formulaire valide"""
        data = {
            'nom': 'Martin',
            'prenom': 'Paul',
            'age': 30,
            'genre': 'Masculin',
            'zone': 'Zone 2',
            'adresse': 'Rue de la Liberté',
            'telephone': '+225987654321',
            'competences': 'Commerce',
            'numero_cni': 'CI987654321'
        }
        form = JeuneForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_age(self):
        """Test la validation de l'âge"""
        data = {
            'nom': 'Martin',
            'prenom': 'Paul',
            'age': 10,  # Âge invalide
            'genre': 'Masculin',
            'zone': 'Zone 2',
            'adresse': 'Rue de la Liberté',
            'telephone': '+225987654321',
            'competences': 'Commerce',
            'numero_cni': 'CI987654321'
        }
        form = JeuneForm(data=data)
        self.assertFalse(form.is_valid())


class JeuneViewTest(TestCase):
    """Tests pour les vues du module de recensement"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.jeune = Jeune.objects.create(
            nom='Dupont',
            prenom='Jean',
            age=25,
            genre='Masculin',
            zone='Zone 1',
            adresse='123 Rue de la Paix',
            telephone='+225123456789',
            competences='Informatique',
            numero_cni='CI123456789'
        )
    
    def test_jeune_list_view(self):
        """Test la vue de liste des jeunes"""
        response = self.client.get(reverse('jeune_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensement/jeune_list.html')
    
    def test_jeune_detail_view(self):
        """Test la vue de détail d'un jeune"""
        response = self.client.get(reverse('jeune_detail', args=[self.jeune.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensement/jeune_detail.html')
    
    def test_jeune_create_view_get(self):
        """Test l'accès au formulaire de création"""
        response = self.client.get(reverse('jeune_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensement/jeune_form.html')
    
    def test_jeune_update_view_get(self):
        """Test l'accès au formulaire de modification"""
        response = self.client.get(reverse('jeune_update', args=[self.jeune.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recensement/jeune_form.html')

