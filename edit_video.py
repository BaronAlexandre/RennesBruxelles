"""
Montage automatique style YouTubeur :
- Suppression des silences et blancs
- Suppression des hésitations (sons courts <0.3s)
- Légère marge conservée autour des prises de parole

Usage :
    py edit_video.py <chemin_video>
    py edit_video.py  (sans argument = utilise VIDEO_INPUT ci-dessous)
"""

import subprocess
import sys
import shutil
from pathlib import Path

# --- Config ---
VIDEO_INPUT = r"C:\Users\Alexandre\AppData\Local\Microsoft\Windows\INetCache\IE\A005WI0W\IMG_0234[1].MOV"

# Seuil de silence (% du volume max). Augmenter si trop de coupures, baisser si blancs résiduels.
SILENCE_THRESHOLD = "4%"

# Marge conservée avant/après chaque prise de parole (en secondes)
# 0.2s = coupe franche style YouTube, 0.3-0.4s = plus naturel
MARGIN = "0.2sec"

# Vitesse de lecture des silences (1 = supprimé, >1 = accéléré au lieu de supprimé)
# 99999 = suppression totale
SILENT_SPEED = "99999"
# ---------------


def check_auto_editor():
    if shutil.which("auto-editor"):
        return True
    result = subprocess.run(
        [sys.executable, "-m", "auto_editor", "--version"],
        capture_output=True,
    )
    return result.returncode == 0


def install_auto_editor():
    print("Installation de auto-editor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "auto-editor"])


def run_edit(input_path: str):
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Fichier introuvable : {input_file}")
        sys.exit(1)

    output_file = input_file.parent / f"{input_file.stem}_monté{input_file.suffix}"

    print(f"Source  : {input_file}")
    print(f"Sortie  : {output_file}")
    print(f"Seuil   : {SILENCE_THRESHOLD}  |  Marge : {MARGIN}")
    print()

    cmd = [
        sys.executable, "-m", "auto_editor",
        str(input_file),
        "--edit", f"audio:threshold={SILENCE_THRESHOLD}",
        "--margin", MARGIN,
        "--silent-speed", SILENT_SPEED,
        "--output", str(output_file),
    ]

    print("Lancement du montage...\n")
    subprocess.run(cmd, check=True)

    print(f"\nFini ! Vidéo montée : {output_file}")


if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else VIDEO_INPUT

    if not check_auto_editor():
        install_auto_editor()

    run_edit(video)
