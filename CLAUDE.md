# RennesBruxelles — Road trip vélo 5 jours

Repo de préparation du trajet vélo Rennes → Bruxelles, 14–18 mai 2026, ~680–700 km en solo.

## Contexte du trip

| | |
|---|---|
| Distance totale | ~680–700 km |
| Durée | 5 jours consécutifs |
| Dates | Mercredi 14 → Dimanche 18 mai 2026 |
| Vitesse cible | 15–18 km/h (endurance, pas de performance) |
| Temps vélo/jour | 4h30 → 6h30 max |
| Dénivelé | Vallonné J1–J2, roulant J3–J5 |

Philosophie : finir chaque journée avec encore "un peu sous le pied". Intensité contrôlée, jamais en force.

## Étapes

| Jour | Date | Trajet | Distance | Départ |
|------|------|--------|----------|--------|
| J1 | Mer 14 mai | Rennes → Flers | ~140 km | 08h00 |
| J2 | Jeu 15 mai | Flers → Rouen | ~180 km | 07h30 |
| J3 | Ven 16 mai | Rouen → Amiens | ~120 km | 08h30 |
| J4 | Sam 17 mai | Amiens → Valenciennes | ~130 km | 08h00 |
| J5 | Dim 18 mai | Valenciennes → Bruxelles | ~110–120 km | 08h30 |

J2 est la journée critique (180 km, fatigue cumulée). J3 est récupération active.

## Logements

| Nuit | Ville | Adresse | Hôte |
|------|-------|---------|------|
| 14→15 mai | Flers | 523 Buisson Corblin, 61100 | Franck |
| 15→16 mai | Rouen | 13 Rue Mogador, 76000 | Le Medicis |
| 16→17 mai | Amiens | 6 Rue Florimond Leroux, 80000 | Ryad |
| 17→18 mai | Valenciennes | 6 Rue de la Gare de Marly, 59300 | Ruth Andrea |

## Retour — Bruxelles → Rennes (mardi 19 mai)

**Train 1 — OUIGO n°54**
- 13h38 Bruxelles-Midi → 16h42 Paris Gare du Nord (3h04)
- Référence : `6HNCGZ` — billet dispo 4 jours avant, à télécharger
- Espace vélo payant

**Correspondance Paris** (~3h15)
- Gare du Nord → Gare Montparnasse avec le vélo
- Prévoir 45–60 min de transfert, taxi recommandé

**Train 2 — TGV INOUI n°8751**
- 19h57 Gare Montparnasse → 21h25 Gare de Rennes (1h28)
- Référence : `JYENLG` — Voiture 18, Place 801, fenêtre, espace vélo inclus

## Fichiers du repo

- `create_komoot_routes.py` — génère les 5 routes via OSRM et les upload sur Komoot en GPX. Identifiants Komoot hardcodés (JWT + cookies). Trouve aussi la ville de pause midi à mi-chemin de chaque étape via Nominatim.
- `instagram_content_plan.md` — plan de contenu Instagram pour les 5 jours du trajet.
- `visuels/instagram.html` — aperçu visuel des posts Instagram.

## Règles d'effort (non négociables)

- Manger toutes les 45 min (banane / barre / pain+miel)
- Boire 500–750 ml/heure (1 bidon eau + 1 bidon sucré)
- Pause courte 5–10 min toutes les 1h30, pause midi 30 min max
- Indicateur : si tu ne peux plus parler en roulant → trop vite
- Cadence fluide > force, jamais de côte en danseuse en force
