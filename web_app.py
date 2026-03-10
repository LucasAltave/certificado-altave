from __future__ import annotations

import sys
import secrets
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "web_app" / "templates"
STATIC_DIR = BASE_DIR / "web_app" / "static"
PREVIEW_DIR = STATIC_DIR / "_previews"

PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR))

from cert_gen import generate_certificate_pdf, generate_certificate_png  # noqa: E402

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static",
)
app.secret_key = "troque_isto_por_algo_seguro"


def _clean(text: str) -> str:
    return (text or "").strip()


def _valid_date_ddmmyyyy(s: str) -> bool:
    try:
        datetime.strptime(s, "%d/%m/%Y")
        return True
    except Exception:
        return False


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/preview")
def preview():
    full_name = _clean(request.form.get("full_name"))
    role = _clean(request.form.get("role"))
    company_name = _clean(request.form.get("company_name"))
    instructor = _clean(request.form.get("instructor"))
    date_text = _clean(request.form.get("date_text"))

    if not full_name or not role or not company_name or not instructor or not date_text:
        return jsonify({"ok": False, "error": "Preencha todos os campos para visualizar."}), 400

    if not _valid_date_ddmmyyyy(date_text):
        return jsonify({"ok": False, "error": "Data inválida. Use DD/MM/AAAA."}), 400

    try:
        preview_name = f"preview_{secrets.token_hex(8)}.png"
        preview_path = generate_certificate_png(
            full_name=full_name,
            role=role,
            company_name=company_name,
            date_text=date_text,
            instructor=instructor,
            output_dir=PREVIEW_DIR,
            filename=preview_name,
        )
        url = url_for("static", filename=f"_previews/{preview_path.name}")
        return jsonify({"ok": True, "url": url})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.post("/generate")
def generate():
    full_name = _clean(request.form.get("full_name"))
    role = _clean(request.form.get("role"))
    company_name = _clean(request.form.get("company_name"))
    instructor = _clean(request.form.get("instructor"))
    date_text = _clean(request.form.get("date_text"))

    if not full_name or not role or not company_name or not instructor or not date_text:
        flash("Preencha todos os campos.")
        return redirect(url_for("index"))

    if not _valid_date_ddmmyyyy(date_text):
        flash("Data inválida. Use o formato DD/MM/AAAA.")
        return redirect(url_for("index"))

    try:
        pdf_path = generate_certificate_pdf(
            full_name=full_name,
            role=role,
            company_name=company_name,
            date_text=date_text,
            instructor=instructor,
        )

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=pdf_path.name,
            mimetype="application/pdf",
        )
    except Exception as e:
        flash(f"Erro ao gerar certificado: {e}")
        return redirect(url_for("index"))


@app.get("/favicon.ico")
def favicon():
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
    if __name__ == "__main__":
    import os

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=False,
    )
