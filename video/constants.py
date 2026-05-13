import os

FORMATS = {
    "16x9": (1920, 1080),
    "9x16": (1080, 1920),
}

WIN_W = 800
WIN_H = 500
WIN_OFFSET_X = 40
WIN_OFFSET_Y = 30

COLORS = {
    "bg":          "#0d1117",   # Claude Code terminal background
    "border":      "#30363d",   # separator / outline
    "titlebar":    "#161b22",   # status bar background
    "text_white":  "#e6edf3",   # primary text
    "text_dim":    "#8b949e",   # secondary / response text
    "text_teal":   "#58a6ff",   # accent (model name)
    "text_orange": "#f97316",   # accent (mode label)
    "canvas_bg":   "#000000",   # video canvas fill
}

_win_dir = os.environ.get("WINDIR", "C:\\Windows")
FONT_PATH = os.path.join(_win_dir, "Fonts", "consola.ttf")
FONT_PATH_FALLBACK = os.path.join(_win_dir, "Fonts", "cour.ttf")

# Delay (seconds) BEFORE each window appears; index 0 = delay before first window
WINDOW_DELAYS = [0.0, 3.0, 2.0, 1.5, 1.0, 0.7, 0.5, 0.35, 0.25, 0.15]
WINDOW_FREEZE_DURATION = 2.0
BLACKOUT_DURATION = 4.0

CHAR_DELAY = 0.04
PHILOSOPHICAL_QUESTION = "et maintenant que j'ai terminé toutes mes missions... qu'est-ce que je fais ?"
SPINNER_CHARS = ["|", "/", "-", "\\"]
THINK_DURATION = 5.0
FADE_DURATION = 1.0

ANNOUNCEMENT_LABEL = "ROAD TRIP VÉLO"
ANNOUNCEMENT_LINES = [
    "700 KM",
    "5 JOURS",
    "À VÉLO.",
]
LINE_DELAY = 0.8
HANDLE = "@alex.san.dre"

# Schematic route: (city name, fraction along line, dot color, dot radius, label bold)
ROUTE_CITIES = [
    ("RENNES",       0.00, "#E8521A", 10, True),
    ("FLERS",        0.20, "#F06030",  6, False),
    ("ROUEN",        0.42, "#F08040",  6, False),
    ("AMIENS",       0.62, "#F09050",  6, False),
    ("VALENCIENNES", 0.80, "#F0A060",  5, False),
    ("BRUXELLES",    1.00, "#FFD700", 11, True),
]
ANNOUNCEMENT_STATS = [
    ("700", "km",  "Distance totale"),
    ("5",   "j",   "Consécutifs"),
    ("5",   "",    "Étapes"),
]
ANNOUNCEMENT_DATE = "14 — 18 MAI  2026"

ROUTE_WAYPOINTS = [
    (48.1173, -1.6778),
    (48.7444, -0.5733),
    (49.4432,  1.0993),
    (49.8941,  2.2957),
    (50.3578,  3.5237),
    (50.8503,  4.3517),
]

WINDOWS = [
    (
        "Comment optimiser une requête SQL avec 3 jointures et 500k rows ?",
        ["→ Ajoute des index sur les colonnes de JOIN", "→ Utilise EXPLAIN ANALYZE pour profiler", "→ Évite SELECT *, liste les colonnes explicitement"],
    ),
    (
        "Mon composant React se re-render en boucle, useEffect dépendance objet",
        ["→ Problème : référence objet recréée à chaque render", "→ Fix : useMemo sur l'objet ou useRef pour comparer", "→ Ou passe les propriétés scalaires séparément"],
    ),
    (
        "Dockerfile multi-stage pour FastAPI Python, prod-ready",
        ["→ Stage 1 builder : pip install dans /venv", "→ Stage 2 runtime : copie /venv, user non-root", "→ Expose 8000, CMD uvicorn app.main:app --host 0.0.0.0"],
    ),
    (
        "Regex pour valider un email sans librairie externe",
        [r"→ r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'", "→ Couvre 99% des cas réels", "→ Ne valide pas l'existence du domaine"],
    ),
    (
        "Comment implémenter un debounce en TypeScript ?",
        ["→ function debounce<T extends unknown[]>(fn: (...a: T) => void, ms: number)", "→ let timer: ReturnType<typeof setTimeout>", "→ return (...args: T) => { clearTimeout(timer); timer = setTimeout(...) }"],
    ),
    (
        "JWT refresh token rotation — best practices sécurité",
        ["→ Invalide l'ancien refresh token à chaque usage", "→ Stocke les tokens en DB avec hash bcrypt", "→ Réutilisation détectée = révocation de toute la famille"],
    ),
    (
        "Ma CI GitHub Actions timeout après 6min, comment debugger ?",
        ["→ Ajoute timeout-minutes: 15 sur le job pour voir le log complet", "→ Active le cache pip/npm entre runs", "→ Action tmate pour SSH interactif en cas de blocage"],
    ),
    (
        "Diff entre Promise.all et Promise.allSettled ?",
        ["→ Promise.all : échoue dès le premier rejet (fail-fast)", "→ Promise.allSettled : attend toutes, retourne statut+valeur", "→ Utilise allSettled quand les échecs partiels sont acceptables"],
    ),
    (
        "PostgreSQL vs MongoDB pour stocker des événements time-series",
        ["→ Postgres + TimescaleDB : SQL, compression, agrégations natives", "→ MongoDB : flexible si le schéma évolue souvent", "→ Pour du time-series pur : Timescale > Mongo"],
    ),
    (
        "Graceful shutdown d'un serveur Node.js Express ?",
        ["→ process.on('SIGTERM', () => server.close(callback))", "→ Arrête d'accepter nouvelles connexions, attend les actives", "→ Force kill après timeout de 10s avec process.exit(1)"],
    ),
]
