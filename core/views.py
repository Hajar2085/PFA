from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Matiere, Cours, Commentaire, Progression
from .forms import MatiereForm, CoursForm
import json
import PyPDF2
import re
from openai import OpenAI

def list_matieres(request):
    """Affiche la liste de toutes les matières."""
    matieres = Matiere.objects.all()
    return render(request, 'core/list_matieres.html', {'matieres': matieres})

def list_cours(request, matiere_id):
    """Affiche les cours associés à une matière spécifique."""
    matiere = get_object_or_404(Matiere, id=matiere_id)
    # Utilisation du related_name 'cours' défini dans le modèle
    cours = matiere.cours.all().order_by('-date_ajout')
    videos = matiere.videos.all().order_by('-date_ajout')
    return render(request, 'core/list_cours.html', {
        'matiere': matiere,
        'cours': cours,
        'videos': videos,
    })

def detail_cours(request, cours_id):
    """Affiche les détails d'un cours et ses commentaires."""
    cours = get_object_or_404(Cours, id=cours_id)
    commentaires = cours.commentaires.all().order_by('-date_creation')
    
    progression = None
    if request.user.is_authenticated:
        # On tente de récupérer la progression de l'étudiant pour ce cours
        progression = Progression.objects.filter(etudiant=request.user, cours=cours).first()

    return render(request, 'core/detail_cours.html', {
        'cours': cours,
        'commentaires': commentaires,
        'progression': progression
    })

@login_required
def marquer_termine(request, cours_id):
    """Marque un cours comme terminé pour l'étudiant connecté (via POST)."""
    if request.method == 'POST':
        cours = get_object_or_404(Cours, id=cours_id)
        
        # S'assurer que seul un étudiant peut avoir une progression
        if request.user.is_etudiant:
            progression, created = Progression.objects.get_or_create(
                etudiant=request.user,
                cours=cours,
                defaults={'est_termine': True}
            )
            # Si la progression existait déjà, on s'assure qu'elle est bien à True
            if not created:
                progression.est_termine = True
                progression.save()
            
    return redirect('detail_cours', cours_id=cours_id)

@login_required
def ajouter_commentaire(request, cours_id):
    """Ajoute un commentaire à un cours (via POST)."""
    if request.method == 'POST':
        cours = get_object_or_404(Cours, id=cours_id)
        texte = request.POST.get('texte', '').strip()
        
        if texte:
            Commentaire.objects.create(
                texte=texte,
                cours=cours,
                auteur=request.user
            )
            
    return redirect('detail_cours', cours_id=cours_id)

@login_required
def ajouter_matiere(request):
    if not request.user.is_professeur:
        return redirect('list_matieres')
    
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_matieres')
    else:
        form = MatiereForm()
    return render(request, 'core/formulaire.html', {'form': form, 'titre': 'Ajouter une matière', 'btn_text': 'Créer la matière'})

@login_required
def ajouter_cours(request):
    if not request.user.is_professeur:
        return redirect('list_matieres')
        
    if request.method == 'POST':
        # request.FILES important pour le champ fichier_pdf !
        form = CoursForm(request.POST, request.FILES)
        if form.is_valid():
            nouvel_objet = form.save()
            return redirect('list_cours', matiere_id=nouvel_objet.matiere.id)
    else:
        # Si on arrive depuis une matière spécifique, on peut pré-remplir
        matiere_id = request.GET.get('matiere')
        initial_data = {}
        if matiere_id:
            initial_data['matiere'] = matiere_id
        form = CoursForm(initial=initial_data)
        
    return render(request, 'core/formulaire.html', {'form': form, 'titre': 'Ajouter un cours', 'btn_text': 'Publier le cours'})

@login_required
def ai_quiz(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text() or ""
                # Nettoyage simple pour supprimer les espaces excessifs
                page_text = re.sub(r' +', ' ', page_text)
                text += page_text + "\n"
                if len(text) > 12000: # Stop early if we have enough content
                    break
            
            text = text.strip()
            if not text:
                raise ValueError("Le PDF ne contient pas de texte lisible (il s'agit peut-être d'un document scanné ou d'une image).")
            
            text = text[:12000]

            client = OpenAI(
              base_url = "https://integrate.api.nvidia.com/v1",
              api_key = "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"
            )

            prompt = f"""You are an elite academic assessor. Generate a 10-question multiple-choice quiz based ONLY on the CORE ACADEMIC CONCEPTS of the provided text.

RULES:
1. FOCUS ON CONTENT: Ask about theories, mechanisms, facts, and logic.
2. ABSOLUTELY NO METADATA: Ignore authors, PDF technical details, or page numbers.
3. OUTPUT: Return ONLY a valid JSON array.

SCHEMA:
[
  {{
    "id": 1,
    "question_text": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer_index": 0, 
    "explanation": "..."
  }}
]

TEXT TO ANALYZE:
{text}"""

            # Switched to meta/llama-3.3-70b-instruct for reliability on NVIDIA API
            completion = client.chat.completions.create(
              model="meta/llama-3.3-70b-instruct",
              messages=[{"role":"user","content":prompt}],
              temperature=0.2,
              max_tokens=4000,
              stream=False,
              timeout=150
            )

            # Safety check to avoid 'NoneType' errors
            if not completion.choices or not completion.choices[0].message:
                raise ValueError("L'IA n'a pas pu générer de réponse. Veuillez réessayer.")

            content = completion.choices[0].message.content or ""
            
            # Print response length for debugging
            print(f"AI Response received. Length: {len(content)} characters.")
            
            # Robust JSON extraction
            start_ptr = content.find('[')
            end_ptr = content.rfind(']')
            if start_ptr != -1 and end_ptr != -1:
                content = content[start_ptr:end_ptr+1]
            else:
                match = re.search(r'\[.*\]', content, re.DOTALL)
                if match:
                    content = match.group(0)
                else:
                    raise ValueError("Format JSON invalide. L'IA n'a pas renvoyé de liste de questions.")
            
            quiz_data = json.loads(content)
            
            return render(request, 'core/ai_quiz_play.html', {'quiz_data': json.dumps(quiz_data)})
        except Exception as e:
            return render(request, 'core/ai_quiz_upload.html', {'error': str(e)})

    return render(request, 'core/ai_quiz_upload.html')
