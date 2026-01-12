from django.urls import path
from .views import (
    JeuneCreateView,
    JeuneListView,
    JeuneDetailView,
    JeuneUpdateView,
    JeuneDeleteView,
    JeuneSuccessView,
)



urlpatterns = [
    # Liste de tous les jeunes
    path('jeunes/', JeuneListView.as_view(), name='jeune_list'),
    
    # Créer un nouveau jeune
    path('jeunes/nouveau/', JeuneCreateView.as_view(), name='jeune_create'),
    
    # Page de succès après enregistrement
    path('jeunes/<int:pk>/success/', JeuneSuccessView.as_view(), name='jeune_success'),
    
    # Voir les détails d'un jeune
    path('jeunes/<int:pk>/', JeuneDetailView.as_view(), name='jeune_detail'),
    
    # Modifier les informations d'un jeune
    path('jeunes/<int:pk>/modifier/', JeuneUpdateView.as_view(), name='jeune_update'),
    
    # Supprimer un jeune
    path('jeunes/<int:pk>/supprimer/', JeuneDeleteView.as_view(), name='jeune_delete'),
]
