from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1920, 1080

BG          = "#0d1117"
SEPARATOR   = "#30363d"
TEXT_MAIN   = "#e6edf3"
TEXT_DIM    = "#8b949e"
TEXT_TEAL   = "#58a6ff"
TEXT_ORANGE = "#f97316"
TEXT_BLUE   = "#79c0ff"
BAR_BG      = "#161b22"
LOGO_COLOR  = "#E8521A"

img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "consola.ttf")
try:
    font        = ImageFont.truetype(font_path, 18)
    font_small  = ImageFont.truetype(font_path, 14)
    font_status = ImageFont.truetype(font_path, 16)
except Exception:
    font = font_small = font_status = ImageFont.load_default()

# --- Pixel-art Claude Code logo ---
LOGO_X, LOGO_Y = 60, 60
P = 7  # pixel size
logo = [
    "  ██████  ",
    " ████████ ",
    "██████████",
    "██ ████ ██",
    "██ ████ ██",
    "██████████",
    " ████████ ",
    "  ██  ██  ",
    "  ██  ██  ",
]
for row_i, row in enumerate(logo):
    for col_i, ch in enumerate(row):
        if ch == "█":
            x0 = LOGO_X + col_i * P
            y0 = LOGO_Y + row_i * P
            draw.rectangle([x0, y0, x0 + P - 1, y0 + P - 1], fill=LOGO_COLOR)

LOGO_W = len(logo[0]) * P
TEXT_X = LOGO_X + LOGO_W + 20

# --- Header info ---
draw.text((TEXT_X, LOGO_Y + 2),  "Claude Code  v2.1.133",          fill=TEXT_MAIN,  font=font)
draw.text((TEXT_X, LOGO_Y + 28), "Sonnet 4.6 · Claude Pro",        fill=TEXT_DIM,   font=font_small)
draw.text((TEXT_X, LOGO_Y + 48), "~/Documents/RennesBruxellesVelo", fill=TEXT_DIM,   font=font_small)

# --- Separator ---
SEP_Y = LOGO_Y + LOGO_W + 16
draw.line([(0, SEP_Y), (W, SEP_Y)], fill=SEPARATOR, width=1)

# --- Prompt ---
draw.text((LOGO_X, SEP_Y + 28), ">", fill=TEXT_MAIN, font=font)

# --- Bottom status bar ---
BAR_Y = H - 36
draw.rectangle([0, BAR_Y, W, H], fill=BAR_BG)
draw.line([(0, BAR_Y), (W, BAR_Y)], fill=SEPARATOR, width=1)

sy = BAR_Y + 9
x = LOGO_X
draw.text((x, sy), "Sonnet 4.6",            fill=TEXT_TEAL,   font=font_status); x += 130
draw.text((x, sy), "|",                     fill=TEXT_DIM,    font=font_status); x += 20
draw.text((x, sy), "RennesBruxellesVelo",   fill=TEXT_ORANGE, font=font_status); x += 220
draw.text((x, sy), "|",                     fill=TEXT_DIM,    font=font_status); x += 20
draw.text((x, sy), "think/high",            fill=TEXT_ORANGE, font=font_status)
draw.text((W - 310, sy), "/ide for Visual Studio Code", fill=TEXT_BLUE, font=font_status)

os.makedirs("assets", exist_ok=True)
img.save("assets/intro.png")
print("Created assets/intro.png")
