import os
from dotenv import load_dotenv

load_dotenv()

def required(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise RuntimeError(f"Variável obrigatória não configurada no .env: {name}")
    return v

SENDGRID_API_KEY = required("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = required("SENDGRID_FROM_EMAIL")

FROM_NAME = os.getenv("FROM_NAME", "Certificados").strip()
SUBJECT = os.getenv("SUBJECT", "Seu certificado foi gerado").strip()

EMAIL_BODY = os.getenv(
    "EMAIL_BODY",
    "Olá! Segue seu certificado em anexo.\n\nAtenciosamente,\nEquipe"
)
EMAIL_BODY = EMAIL_BODY.replace("\\n", "\n")