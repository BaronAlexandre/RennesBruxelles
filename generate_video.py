# generate_video.py
import os
import sys
from moviepy.editor import concatenate_videoclips

from video.constants import FORMATS
from video.scenes import (
    make_intro_clip,
    make_windows_clip,
    make_blackout_clip,
    make_philosophical_clip,
    make_announcement_clip,
)

# Locate intro asset
ASSET = next(
    (p for p in ["assets/intro.mp4", "assets/intro.png", "assets/intro.jpg"] if os.path.exists(p)),
    None,
)
if ASSET is None:
    print("ERROR: place your intro capture at assets/intro.mp4 or assets/intro.png")
    sys.exit(1)

for fmt_name, (w, h) in FORMATS.items():
    print(f"\n=== {fmt_name}  {w}x{h} ===")

    clips = [
        make_intro_clip(w, h, asset_path=ASSET),
        make_windows_clip(w, h),
        make_blackout_clip(w, h),
        make_philosophical_clip(w, h),
        make_announcement_clip(w, h),
    ]

    final = concatenate_videoclips(clips, method="compose")
    out = f"annonce_{fmt_name}.mp4"
    print(f"Rendering {out}  (duration: {final.duration:.1f}s) ...")
    final.write_videofile(
        out,
        fps=30,
        codec="libx264",
        audio=False,
        preset="medium",
        ffmpeg_params=["-crf", "18"],
        logger=None,
    )
    print(f"Saved {out}")
    final.close()
    for c in clips:
        c.close()

print("\nDone. Files: annonce_16x9.mp4  annonce_9x16.mp4")
