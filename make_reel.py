"""
Crée RenneBruxelles_reel.mp4 :
  - format 9:16 (crop centré depuis 3840x2160)
  - sous-titres brûlés (style Instagram : blanc, contour noir, bas de cadre)
  - audio original conservé
  - original non modifié
"""

import json, subprocess, os, imageio_ffmpeg

# ── Chemins ─────────────────────────────────────────────────────────────────
BASE    = r'C:\Users\Alexandre\Documents\RennesBruxellesVelo'
SRC     = os.path.join(BASE, 'RenneBruxelles.mp4')
OUT     = os.path.join(BASE, 'RenneBruxelles_reel.mp4')
SRT     = os.path.join(BASE, 'subtitles.srt')
FFMPEG  = imageio_ffmpeg.get_ffmpeg_exe()

# ── Générer le SRT ───────────────────────────────────────────────────────────
def fmt_ts(sec):
    h  = int(sec // 3600)
    m  = int((sec % 3600) // 60)
    s  = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

with open(os.path.join(BASE, 'transcription.json'), encoding='utf-8') as f:
    data = json.load(f)

with open(SRT, 'w', encoding='utf-8') as f:
    for i, seg in enumerate(data['segments'], 1):
        text = seg['text'].strip()
        f.write(f"{i}\n")
        f.write(f"{fmt_ts(seg['start'])} --> {fmt_ts(seg['end'])}\n")
        f.write(f"{text}\n\n")

print(f'SRT written: {len(data["segments"])} segments')

# ── Paramètres crop 9:16 ────────────────────────────────────────────────────
# Source : 3840x2160.  Garder la hauteur entière, réduire la largeur à 9/16
src_w, src_h = 3840, 2160
crop_w = round(src_h * 9 / 16)          # 1215
crop_x = (src_w - crop_w) // 2          # 1312 — centré horizontalement
crop_filter = f'crop={crop_w}:{src_h}:{crop_x}:0,scale=1080:1920'

# ── Style sous-titres ────────────────────────────────────────────────────────
# ForceStyle : Police Barlow Condensed si dispo, sinon Arial Bold
# Taille 22 = ~55px à 1080p avec le crop — lisible sur mobile
# Outline 2px noir, fond semi-transparent
srt_escaped = SRT.replace('\\', '/').replace(':', '\\:')
sub_filter  = (
    f"subtitles='{srt_escaped}'"
    f":force_style='Fontname=Arial,Bold=1,Fontsize=22,"
    f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
    f"Outline=2,Shadow=1,Alignment=2,MarginV=40'"
)

vf = f"{crop_filter},{sub_filter}"

# ── Commande ffmpeg ──────────────────────────────────────────────────────────
cmd = [
    FFMPEG, '-y',
    '-i', SRC,
    '-vf', vf,
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '23',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-movflags', '+faststart',
    OUT
]

print('Starting ffmpeg export...')
print('Command:', ' '.join(cmd[:6]) + ' ...')
result = subprocess.run(cmd, capture_output=False)

if result.returncode == 0:
    size_mb = os.path.getsize(OUT) / (1024*1024)
    print(f'\nDone! Output: {OUT}')
    print(f'Size: {size_mb:.1f} MB')
else:
    print(f'ffmpeg failed with code {result.returncode}')
