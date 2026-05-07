# Design — Vidéo d'annonce Rennes → Bruxelles

**Date** : 2026-05-08  
**Output** : `annonce_16x9.mp4` + `annonce_9x16.mp4`  
**Stack** : Python, moviepy, Pillow, staticmap

---

## Structure de la vidéo (~35 secondes)

| # | Acte | Durée | Description |
|---|------|-------|-------------|
| 1 | Intro coding | ~3s | Capture réelle fournie par l'utilisateur (vidéo ou image fixe), fondu entrant |
| 2 | Accumulation fenêtres | ~10s | 10 fenêtres Claude Code apparaissent en accélération exponentielle, elles se stackent avec décalage de position |
| 3 | Freeze burnout | ~2s | Toutes les fenêtres visibles, écran saturé, freeze |
| 4 | Fond noir | 4s | Fondu vers noir complet |
| 5 | Question philosophique | ~8s | Fenêtre Claude Code seule, question typée caractère par caractère, spinner "Thinking…" 5s, fondu noir |
| 6 | Annonce | ~6s | Texte ligne par ligne puis carte OSM du tracé, @alex.san.dre en bas |

---

## Acte 2 — Timing d'accélération

| Fenêtre | Délai avant apparition |
|---------|----------------------|
| 1 | 3.0s |
| 2 | 2.0s |
| 3 | 1.5s |
| 4 | 1.0s |
| 5 | 0.7s |
| 6 | 0.5s |
| 7 | 0.35s |
| 8 | 0.25s |
| 9 | 0.15s |
| 10 | 0.08s |

---

## Rendu visuel des fenêtres Claude Code

- **Fond fenêtre** : `#1a1a1a`, bordure `#333`, coins arrondis 8px
- **Barre de titre** : gris foncé, 3 dots macOS (rouge `#FF5F57`, jaune `#FFBD2E`, vert `#28CA41`)
- **Police** : `Cascadia Code` / `JetBrains Mono` / fallback `Courier New`
- **Prompt** : `> ` + question en blanc
- **Réponse** : texte `#a0a0a0`, mots-clés en orange `#E8521A`
- **Taille** : 800×500px par fenêtre
- **Stack offset** : +40px x, +30px y à chaque nouvelle fenêtre

### 10 questions dev (rédigées dans le script)

1. `> Comment optimiser une requête SQL avec 3 jointures et 500k rows ?`
2. `> Mon composant React se re-render en boucle, useEffect avec une dépendance objet`
3. `> Dockerfile multi-stage pour une app Python FastAPI, prod-ready`
4. `> Regex pour valider un email sans librairie externe`
5. `> Comment implémenter un debounce en TypeScript ?`
6. `> JWT refresh token rotation — best practices sécurité`
7. `> Ma CI GitHub Actions timeout après 6min, comment debugger ?`
8. `> Diff entre Promise.all et Promise.allSettled, quand utiliser lequel ?`
9. `> PostgreSQL vs MongoDB pour stocker des événements time-series`
10. `> Comment faire un graceful shutdown d'un serveur Node.js Express ?`

---

## Acte 5 — Scène philosophique

- Fenêtre Claude Code seule, centrée sur fond noir
- Typewriter : `> et maintenant que j'ai terminé toutes mes missions... qu'est-ce que je fais ?`
  - Vitesse : 40ms/caractère
- 0.5s pause après dernier caractère
- Spinner `⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏` + texte `Thinking…` pendant 5s
- Fondu noir 1s

---

## Acte 6 — Annonce finale

Texte ligne par ligne sur fond noir (0.8s entre chaque) :
```
Rennes → Bruxelles
680 km · 5 jours
14 — 18 mai 2026
```
Puis carte OSM en fondu :
- Tracé : Rennes → Flers → Rouen → Amiens → Valenciennes → Bruxelles
- Générée via `staticmap` Python
- 5 étapes marquées

`@alex.san.dre` apparaît en bas en dernier.

---

## Formats de sortie

- `annonce_16x9.mp4` — 1920×1080, 30fps
- `annonce_9x16.mp4` — 1080×1920, 30fps (recadrage vertical avec adaptation des positions)

---

## Assets requis

- `assets/intro.mp4` ou `assets/intro.png` — capture de l'intro coding (fournie par l'utilisateur)
- Police monospace installée ou embarquée dans `assets/`

---

## Dépendances Python

```
moviepy
Pillow
staticmap
requests
numpy
```
