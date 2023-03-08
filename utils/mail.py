from __future__ import annotations

import smtplib
import typing
from email.message import EmailMessage

from utils.models import Email

if typing.TYPE_CHECKING:
    from client.environment import ENVIRONMENT


__all__: tuple[str, ...] = ("send_email",)


def send_email(
    config: "ENVIRONMENT",
    mail: Email,
) -> None:
    msg = EmailMessage()
    msg["Subject"] = mail.subject
    msg["From"] = mail.email
    msg["To"] = mail.email
    msg.set_content(mail.message)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(str(config.EMAIL_ID), str(config.EMAIL_PASSWORD))
        smtp.send_message(msg)
    return None
