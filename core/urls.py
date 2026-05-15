from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Routes pour l'authentification des étudiants et professeurs
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    # Compat: certains redirects Django pointent sur /accounts/login/
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Routes de l'application Front-Office
    path('', views.list_matieres, name='list_matieres'),
    path('matiere/<int:matiere_id>/', views.list_cours, name='list_cours'),
    path('ajouter-matiere/', views.ajouter_matiere, name='ajouter_matiere'),
    path('ajouter-cours/', views.ajouter_cours, name='ajouter_cours'),
    path('cours/<int:cours_id>/', views.detail_cours, name='detail_cours'),
    path('cours/<int:cours_id>/terminer/', views.marquer_termine, name='marquer_termine'),
    path('cours/<int:cours_id>/commenter/', views.ajouter_commentaire, name='ajouter_commentaire'),
    path('ai-quiz/', views.ai_quiz, name='ai_quiz'),
]
