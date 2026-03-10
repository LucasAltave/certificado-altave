import base64
from pathlib import Path

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition, Email
)

from config import (
    SENDGRID_API_KEY,
    SENDGRID_FROM_EMAIL,
    FROM_NAME,
    SUBJECT,
    EMAIL_BODY,
)

def _guess_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return "application/pdf"
    if suffix == ".png":
        return "image/png"
    if suffix in (".jpg", ".jpeg"):
        return "image/jpeg"
    return "application/octet-stream"

def send_certificate(to_email: str, attachment_path: Path) -> None:
    to_email = (to_email or "").strip()
    if not to_email:
        raise ValueError("to_email vazio")

    attachment_path = Path(attachment_path)
    if not attachment_path.exists():
        raise FileNotFoundError(f"Arquivo de anexo não encontrado: {attachment_path}")

    mime = _guess_mime(attachment_path)

    # Lê e codifica o arquivo em base64
    data = attachment_path.read_bytes()
    encoded = base64.b64encode(data).decode("utf-8")

    message = Mail(
        from_email=Email(SENDGRID_FROM_EMAIL, FROM_NAME),
        to_emails=to_email,
        subject=SUBJECT,
        plain_text_content=EMAIL_BODY,
    )

    attachment = Attachment(
        FileContent(encoded),
        FileName(attachment_path.name),
        FileType(mime),
        Disposition("attachment"),
    )
    message.add_attachment(attachment)

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    resp = sg.send(message)

    # 202 = accepted (o padrão do SendGrid ao aceitar para envio)
    if resp.status_code != 202:
        raise RuntimeError(f"SendGrid falhou: status={resp.status_code} body={resp.body}")

    print(f"[OK] SendGrid aceitou o envio para {to_email}. Status: {resp.status_code}")
