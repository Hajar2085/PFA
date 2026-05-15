from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from core.models import Cours, Matiere, Video


@dataclass(frozen=True)
class SeedCours:
    titre: str


@dataclass(frozen=True)
class SeedVideo:
    titre: str
    youtube_url: str


@dataclass(frozen=True)
class SeedMatiere:
    nom: str
    cours: list[SeedCours]
    videos: list[SeedVideo]


SEED_DATA: list[SeedMatiere] = [
    # Matières "programmation" (>= 10)
    SeedMatiere(
        nom="Programmation Python",
        cours=[
            SeedCours(titre="Python — bases (syntaxe, types, conditions)"),
            SeedCours(titre="Python — fonctions, modules, fichiers"),
        ],
        videos=[
            SeedVideo(titre="Python pour débutants — cours complet", youtube_url="https://www.youtube.com/watch?v=rfscVS0vtbw"),
            SeedVideo(titre="Python — fonctions et modules", youtube_url="https://www.youtube.com/watch?v=9Os0o3wzS_I"),
        ],
    ),
    SeedMatiere(
        nom="Programmation Java",
        cours=[
            SeedCours(titre="Java — POO (classes, objets, encapsulation)"),
            SeedCours(titre="Java — collections et exceptions"),
        ],
        videos=[
            SeedVideo(titre="Java — cours complet (bases)", youtube_url="https://www.youtube.com/watch?v=grEKMHGYyns"),
            SeedVideo(titre="Java — POO expliquée", youtube_url="https://www.youtube.com/watch?v=SS-9y0H3Si8"),
        ],
    ),
    SeedMatiere(
        nom="Programmation C",
        cours=[
            SeedCours(titre="C — bases + pointeurs (introduction)"),
            SeedCours(titre="C — tableaux, chaînes, mémoire"),
        ],
        videos=[
            SeedVideo(titre="C Programming Tutorial for Beginners", youtube_url="https://www.youtube.com/watch?v=KJgsSFOSQv0"),
            SeedVideo(titre="Pointers in C — explained", youtube_url="https://www.youtube.com/watch?v=zuegQmMdy8M"),
        ],
    ),
    SeedMatiere(
        nom="Programmation C++",
        cours=[
            SeedCours(titre="C++ — bases + POO"),
            SeedCours(titre="C++ — STL (vector, map)"),
        ],
        videos=[
            SeedVideo(titre="C++ Tutorial for Beginners", youtube_url="https://www.youtube.com/watch?v=vLnPwxZdW4Y"),
            SeedVideo(titre="STL in C++ — overview", youtube_url="https://www.youtube.com/watch?v=RBSGKlAvoiM"),
        ],
    ),
    SeedMatiere(
        nom="Programmation JavaScript",
        cours=[
            SeedCours(titre="JavaScript — bases (DOM, événements)"),
            SeedCours(titre="JavaScript — async/await, fetch"),
        ],
        videos=[
            SeedVideo(titre="JavaScript Full Course for Beginners", youtube_url="https://www.youtube.com/watch?v=PkZNo7MFNFg"),
            SeedVideo(titre="Async JS Crash Course", youtube_url="https://www.youtube.com/watch?v=PoRJizFvM7s"),
        ],
    ),
    SeedMatiere(
        nom="Développement Web (HTML/CSS)",
        cours=[
            SeedCours(titre="HTML5 — structure et formulaires"),
            SeedCours(titre="CSS3 — flexbox, grid, responsive"),
        ],
        videos=[
            SeedVideo(titre="HTML Full Course", youtube_url="https://www.youtube.com/watch?v=pQN-pnXPaVg"),
            SeedVideo(titre="CSS Full Course", youtube_url="https://www.youtube.com/watch?v=OXGznpKZ_sA"),
        ],
    ),
    SeedMatiere(
        nom="Développement Web (Django)",
        cours=[
            SeedCours(titre="Django — modèles, vues, templates"),
            SeedCours(titre="Django — auth, médias, déploiement (bases)"),
        ],
        videos=[
            SeedVideo(titre="Django Tutorial for Beginners", youtube_url="https://www.youtube.com/watch?v=F5mRW0jo-U4"),
            SeedVideo(titre="Django REST Framework Crash Course", youtube_url="https://www.youtube.com/watch?v=tujhGdn1EMI"),
        ],
    ),
    SeedMatiere(
        nom="Algorithmique",
        cours=[
            SeedCours(titre="Algo — complexité (Big-O) + bases"),
            SeedCours(titre="Algo — tri et recherche"),
        ],
        videos=[
            SeedVideo(titre="Big-O Notation — explained", youtube_url="https://www.youtube.com/watch?v=D6xkbGLQesk"),
            SeedVideo(titre="Sorting Algorithms — overview", youtube_url="https://www.youtube.com/watch?v=kgBjXUE_Nwc"),
        ],
    ),
    SeedMatiere(
        nom="Structures de Données",
        cours=[
            SeedCours(titre="SD — piles, files, listes chaînées"),
            SeedCours(titre="SD — arbres, graphes (intro)"),
        ],
        videos=[
            SeedVideo(titre="Data Structures Easy to Advanced", youtube_url="https://www.youtube.com/watch?v=RBSGKlAvoiM"),
            SeedVideo(titre="Graphs — introduction", youtube_url="https://www.youtube.com/watch?v=gXgEDyodOJU"),
        ],
    ),
    SeedMatiere(
        nom="Bases de Données (SQL)",
        cours=[
            SeedCours(titre="SQL — SELECT, JOIN, GROUP BY"),
            SeedCours(titre="SQL — conception (MLD/MCD) + normalisation"),
        ],
        videos=[
            SeedVideo(titre="SQL Tutorial - Full Database Course", youtube_url="https://www.youtube.com/watch?v=HXV3zeQKqGY"),
            SeedVideo(titre="Database Design — normalization basics", youtube_url="https://www.youtube.com/watch?v=UrYLYV7WSHM"),
        ],
    ),
    SeedMatiere(
        nom="Génie Logiciel (UML)",
        cours=[
            SeedCours(titre="UML — diagrammes (cas d'utilisation, classes)"),
            SeedCours(titre="UML — séquence, activités, bonnes pratiques"),
        ],
        videos=[
            SeedVideo(titre="UML Diagrams Full Course", youtube_url="https://www.youtube.com/watch?v=WnMQ8HlmeXc"),
            SeedVideo(titre="UML Class Diagram Tutorial", youtube_url="https://www.youtube.com/watch?v=UI6lqHOVHic"),
        ],
    ),
    SeedMatiere(
        nom="Git & Collaboration",
        cours=[
            SeedCours(titre="Git — bases (commit, branch, merge)"),
            SeedCours(titre="Git — workflow (pull request, rebase)"),
        ],
        videos=[
            SeedVideo(titre="Git and GitHub for Beginners", youtube_url="https://www.youtube.com/watch?v=RGOj5yH7evk"),
            SeedVideo(titre="Git Branching and Merging", youtube_url="https://www.youtube.com/watch?v=FyAAIHHClqI"),
        ],
    ),

    # Anciens noms déjà présents dans la base (on les alimente aussi)
    SeedMatiere(
        nom="Mathématiques",
        cours=[
            SeedCours(titre="Mathématiques — rappels (fonctions, limites)"),
            SeedCours(titre="Mathématiques — dérivées & applications"),
        ],
        videos=[
            SeedVideo(titre="Fonctions — notions de base", youtube_url="https://www.youtube.com/watch?v=3d6DsjIBzJ4"),
            SeedVideo(titre="Dérivées — comprendre la dérivation", youtube_url="https://www.youtube.com/watch?v=ANyVpMS3HLg"),
        ],
    ),
    SeedMatiere(
        nom="Maths",
        cours=[
            SeedCours(titre="Maths — rappels (fonctions, limites)"),
            SeedCours(titre="Maths — dérivées & exercices"),
        ],
        videos=[
            SeedVideo(titre="Fonctions — notions de base", youtube_url="https://www.youtube.com/watch?v=3d6DsjIBzJ4"),
            SeedVideo(titre="Dérivées — comprendre la dérivation", youtube_url="https://www.youtube.com/watch?v=ANyVpMS3HLg"),
        ],
    ),
    SeedMatiere(
        nom="Physique",
        cours=[
            SeedCours(titre="Physique — cinématique (cours)"),
            SeedCours(titre="Physique — électricité (loi d'Ohm)"),
        ],
        videos=[
            SeedVideo(titre="Cinématique — mouvement rectiligne", youtube_url="https://www.youtube.com/watch?v=Y0V-3p8vZqU"),
            SeedVideo(titre="Électricité — loi d'Ohm", youtube_url="https://www.youtube.com/watch?v=7Z5c0mPpV0o"),
        ],
    ),
    SeedMatiere(
        nom="Informatique",
        cours=[
            SeedCours(titre="Informatique — algorithmique (intro)"),
            SeedCours(titre="Informatique — structures de données (bases)"),
        ],
        videos=[
            SeedVideo(titre="Introduction à l'algorithmique", youtube_url="https://www.youtube.com/watch?v=8hly31xKli0"),
            SeedVideo(titre="Structures de données — bases", youtube_url="https://www.youtube.com/watch?v=bum_19loj9A"),
        ],
    ),
]


class Command(BaseCommand):
    help = "Seed: matières + cours(PDF) + vidéos YouTube"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pdf-source",
            default="media/cours/Gestion_de_réservation_de_salle_Diagramme_classe.pdf",
            help="Chemin du PDF modèle à dupliquer (relatif au projet).",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Si activé, recrée les cours/vidéos même s'ils existent.",
        )

    def handle(self, *args, **options):
        overwrite: bool = bool(options["overwrite"])

        pdf_source_rel = str(options["pdf_source"])
        pdf_source_path = (Path(settings.BASE_DIR) / pdf_source_rel).resolve()
        if not pdf_source_path.exists():
            raise SystemExit(
                f"PDF source introuvable: {pdf_source_path}\n"
                "Astuce: mets un PDF dans media/cours/ puis relance avec --pdf-source."
            )

        target_dir = Path(settings.MEDIA_ROOT) / "cours"
        target_dir.mkdir(parents=True, exist_ok=True)

        created_matieres = 0
        created_cours = 0
        created_videos = 0

        for m in SEED_DATA:
            matiere, mat_created = Matiere.objects.get_or_create(nom=m.nom)
            if mat_created:
                created_matieres += 1

            for c in m.cours:
                existing = Cours.objects.filter(matiere=matiere, titre=c.titre).first()
                if existing and not overwrite:
                    continue
                if existing and overwrite:
                    existing.delete()

                safe_name = (
                    f"{matiere.nom}_{c.titre}".replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                    .replace("—", "-")
                )
                filename = f"{safe_name}.pdf"
                dest_path = target_dir / filename

                if not dest_path.exists() or overwrite:
                    shutil.copyfile(pdf_source_path, dest_path)

                with dest_path.open("rb") as f:
                    cours = Cours(titre=c.titre, matiere=matiere)
                    cours.fichier_pdf.save(filename, File(f), save=True)
                    created_cours += 1

            for v in m.videos:
                existing_v = Video.objects.filter(matiere=matiere, youtube_url=v.youtube_url).first()
                if existing_v and not overwrite:
                    continue
                if existing_v and overwrite:
                    existing_v.delete()

                Video.objects.create(matiere=matiere, titre=v.titre, youtube_url=v.youtube_url)
                created_videos += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed terminé. Matières +{created_matieres}, Cours +{created_cours}, Vidéos +{created_videos}."
            )
        )
