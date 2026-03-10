from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATE_PATH = ASSETS_DIR / "cert_template.png"

PDF_SCALE = 4


# =========================
# CORES
# =========================
BLUE = (18, 61, 150)
DARK_BLUE = (10, 44, 115)
BLACK = (45, 49, 58)
GRAY = (100, 105, 118)


# =========================
# FONTES
# =========================
def _pick_font(candidates: list[str]) -> Optional[Path]:
    for p in candidates:
        path = Path(p)
        if path.exists():
            return path
    return None


REGULAR_FONT_PATH = _pick_font([
    "C:/Windows/Fonts/calibri.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/tahoma.ttf",
    "C:/Windows/Fonts/verdana.ttf",
])

BOLD_FONT_PATH = _pick_font([
    "C:/Windows/Fonts/calibrib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/tahomabd.ttf",
    "C:/Windows/Fonts/verdanab.ttf",
])

SCRIPT_FONT_PATH = _pick_font([
    "C:/Windows/Fonts/segoesc.ttf",
    "C:/Windows/Fonts/calibrii.ttf",
    "C:/Windows/Fonts/ariali.ttf",
])


def _font(size: int, *, bold: bool = False, script: bool = False):
    if script:
        path = SCRIPT_FONT_PATH or REGULAR_FONT_PATH
    elif bold:
        path = BOLD_FONT_PATH or REGULAR_FONT_PATH
    else:
        path = REGULAR_FONT_PATH

    if path and Path(path).exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


# =========================
# HELPERS
# =========================
def _ensure_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} não encontrado em: {path}")


def _text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _draw_center(draw: ImageDraw.ImageDraw, text: str, x_center: int, y: int, font, fill):
    w, _ = _text_size(draw, text, font)
    draw.text((x_center - w // 2, y), text, font=font, fill=fill)


def _fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    start_size: int,
    min_size: int,
    *,
    bold: bool = False,
    script: bool = False,
):
    size = start_size
    font = _font(size, bold=bold, script=script)
    w, _ = _text_size(draw, text, font)

    while w > max_width and size > min_size:
        size -= 1
        font = _font(size, bold=bold, script=script)
        w, _ = _text_size(draw, text, font)

    return font


def _safe_filename(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).strip()
    safe = safe.replace(" ", "_")
    return safe or "certificado"


def _clean_text(value: str, max_len: int) -> str:
    value = (value or "").strip()
    value = " ".join(value.split())
    return value[:max_len]


# =========================
# RENDER PRINCIPAL
# =========================
def render_certificate_image(
    full_name: str,
    role: str,
    date_text: str,
    instructor: str = "Lucas Pereira",
    company_name: str = "ALTAVE",
) -> Image.Image:
    _ensure_file(TEMPLATE_PATH, "Template do certificado")

    full_name = _clean_text(full_name, 120)
    role = _clean_text(role, 80)
    date_text = _clean_text(date_text, 20)
    instructor = _clean_text(instructor, 80)
    company_name = _clean_text(company_name, 90)

    if not full_name or not role or not date_text or not instructor or not company_name:
        raise ValueError("Campos obrigatórios: Nome, Função, Data, Instrutor e Empresa.")

    img = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(img)

    w, h = img.size
    cx = w // 2

    # =========================
    # FONTES AJUSTADAS
    # =========================
    title_font = _font(52, bold=True)
    subtitle_font = _font(20, bold=True)

    intro_font = _font(16)
    name_font = _fit_font(draw, f"Sr(a). {full_name},", int(w * 0.56), 30, 19, bold=True)

    body_font = _font(16)
    body_bold_font = _font(16, bold=True)

    role_prefix_font = _font(16)
    role_value_font = _fit_font(draw, f" {role},", int(w * 0.24), 16, 11, bold=True)

    date_prefix_font = _font(16)
    date_value_font = _fit_font(draw, f" {date_text},", int(w * 0.18), 16, 11, bold=True)

    sign_script_font = _fit_font(draw, instructor, int(w * 0.24), 24, 16, script=True)
    company_font = _fit_font(draw, company_name, int(w * 0.24), 15, 10, bold=True)
    footer_label_font = _font(11, bold=True)

    # =========================
    # TÍTULOS
    # =========================
    _draw_center(draw, "CERTIFICADO", cx, 52, title_font, DARK_BLUE)
    _draw_center(draw, "OPERADOR E REPLICADOR DO SISTEMA", cx, 104, subtitle_font, DARK_BLUE)

    # =========================
    # BLOCO CENTRAL
    # =========================
    y_intro = 185
    y_name = 220
    y_role = 257
    y_line1 = 294
    y_line2 = 331
    y_line3 = 368
    y_line4 = 405

    _draw_center(draw, "Por meio deste, a ALTAVE certifica que", cx, y_intro, intro_font, BLACK)
    _draw_center(draw, f"Sr(a). {full_name},", cx, y_name, name_font, DARK_BLUE)

    # Linha função
    role_prefix = "com a função de"
    role_value = f" {role},"

    prefix_w, _ = _text_size(draw, role_prefix, role_prefix_font)
    value_w, _ = _text_size(draw, role_value, role_value_font)
    total_w = prefix_w + value_w
    start_x = cx - total_w // 2

    draw.text((start_x, y_role), role_prefix, font=role_prefix_font, fill=BLACK)
    draw.text((start_x + prefix_w, y_role), role_value, font=role_value_font, fill=DARK_BLUE)

    _draw_center(
        draw,
        "participou do treinamento de operação e instrução do sistema",
        cx,
        y_line1,
        body_font,
        BLACK,
    )

    # Linha data
    date_prefix = "de Software Altave Harpia no dia"
    date_value = f" {date_text},"

    dp_w, _ = _text_size(draw, date_prefix, date_prefix_font)
    dv_w, _ = _text_size(draw, date_value, date_value_font)
    total2_w = dp_w + dv_w
    start2_x = cx - total2_w // 2

    draw.text((start2_x, y_line2), date_prefix, font=date_prefix_font, fill=BLACK)
    draw.text((start2_x + dp_w, y_line2), date_value, font=date_value_font, fill=DARK_BLUE)

    _draw_center(
        draw,
        "adquirindo com sucesso capacidade de operar o sistema e atuar",
        cx,
        y_line3,
        body_font,
        BLACK,
    )

    _draw_center(
        draw,
        "como replicador de conhecimento do ALTAVE Harpia.",
        cx,
        y_line4,
        body_bold_font,
        fill=DARK_BLUE,
    )

    # =========================
    # RODAPÉ / ASSINATURAS
    # =========================
    left_sign_x = 215
    right_sign_x = 565

    # Ajuste fino vertical
    sign_name_y = 485
    line_label_y = 520

    # Esquerda: instrutor
    _draw_center(draw, instructor, left_sign_x, sign_name_y, sign_script_font, BLUE)
    _draw_center(draw, "Instrutor", left_sign_x, line_label_y, footer_label_font, GRAY)

    # Direita: empresa
    _draw_center(draw, company_name, right_sign_x, sign_name_y, company_font, BLACK)
    _draw_center(draw, "Empresa do Colaborador", right_sign_x, line_label_y, footer_label_font, GRAY)

    return img


# =========================
# SAÍDAS
# =========================
def generate_certificate_pdf(
    full_name: str,
    role: str,
    date_text: str,
    instructor: str = "Lucas Pereira",
    company_name: str = "ALTAVE",
) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    img = render_certificate_image(
        full_name=full_name,
        role=role,
        date_text=date_text,
        instructor=instructor,
        company_name=company_name,
    ).convert("RGB")

    enlarged = img.resize((img.width * PDF_SCALE, img.height * PDF_SCALE), Image.LANCZOS)

    safe_name = _safe_filename(full_name)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUT_DIR / f"certificado_{safe_name}_{ts}.pdf"

    enlarged.save(out_path, "PDF", resolution=300.0)
    return out_path


def generate_certificate_png(
    full_name: str,
    role: str,
    date_text: str,
    instructor: str = "Lucas Pereira",
    company_name: str = "ALTAVE",
    output_dir: Optional[Path] = None,
    filename: Optional[str] = None,
) -> Path:
    target_dir = output_dir or OUTPUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    img = render_certificate_image(
        full_name=full_name,
        role=role,
        date_text=date_text,
        instructor=instructor,
        company_name=company_name,
    )

    if filename:
        out_name = filename
    else:
        safe_name = _safe_filename(full_name)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_name = f"certificado_{safe_name}_{ts}.png"

    out_path = target_dir / out_name
    img.save(out_path, "PNG")
    return out_path


def generate_certificate_image(
    full_name: str,
    role: str,
    date_text: str,
    instructor: str = "Lucas Pereira",
    company_name: str = "ALTAVE",
) -> Path:
    return generate_certificate_pdf(
        full_name=full_name,
        role=role,
        date_text=date_text,
        instructor=instructor,
        company_name=company_name,
    )
