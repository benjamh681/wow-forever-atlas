# Pages de référencement de Travelcraft

Ce dossier n'est pas publié sur le site (GitHub Pages ignore les dossiers qui commencent par « _ »).
Il contient l'outil qui fabrique les pages Trajets et Maîtres de vol dans les trois langues.

## Ce que produit l'outil
- `/routes/`, `/fr/trajets/`, `/es/rutas/` : le sommaire et une page par trajet (liste dans `pairs.py`).
- `/flight-paths/`, `/fr/vols/`, `/es/vuelos/` : tous les maîtres de vol par zone.

## Mettre à jour après un changement de la carte
1. `python3 _build/extract.py` : relit les trajets dans la carte (EN, FR, ES, DE ; l'allemand ajouté le 9 novembre). Supprimer `data.json` avant pour tout recalculer.
2. `python3 _build/extract_fp.py` : relit les maîtres de vol et leurs vols.
3. `python3 _build/build.py .` : réécrit toutes les pages.
4. `python3 _build/check_site.py .` : vérifie les liens.

Il faut Python 3 et Playwright (`pip install playwright` puis `playwright install chromium`).
Textes des pages : `l10n.py`. Ajouter un trajet : une ligne dans `pairs.py`, puis les étapes 1, 3 et 4, et ajouter les nouvelles adresses au sitemap.

Attention (23 octobre) : `extract_fp.py` ne relit que l'anglais, le français et l'espagnol, et sans les champs `lead` et `note`. Le relancer efface l'allemand et les textes des points de vol sans trajet. Pour un petit changement (statut ou texte d'un maître de vol), modifier `fp.json` à la main dans les quatre langues, puis lancer `build.py`.
