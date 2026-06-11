import mimetypes
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from core.logger import logger
from core.settings import settings


class SMTPClient:
    def __init__(
        self,
        host: str = settings.smtp_host,
        port: int = settings.smtp_port,
        sender: str = settings.smtp_sender,
    ) -> None:
        self.host = host
        self.port = port
        self.sender = sender

    def send_mail(self, subject: str, body: str, recipient: str, images: dict | None):
        if not self.__is_active():
            self.__log_suggestions(body)
            return

        msg_root = MIMEMultipart("related")
        msg_root["Subject"] = subject
        msg_root["From"] = self.sender.strip()
        msg_root["To"] = recipient.strip()

        msg_alt = MIMEMultipart("alternative")
        msg_root.attach(msg_alt)

        html_part = MIMEText(body, "html", "utf-8")
        msg_alt.attach(html_part)

        if images:
            for content_id, path in images.items():
                data = Path(path).read_bytes()
                ctype, _ = mimetypes.guess_type(path)
                subtype = ctype.split("/", 1)[1] if ctype else "png"

                img = MIMEImage(data, _subtype=subtype)

                img.add_header("Content-ID", f"<{content_id}>")
                img.add_header("X-Attachment-Id", content_id)
                img.add_header("Content-Disposition", "inline")
                img.add_header("Content-Location", Path(path).name)
                msg_root.attach(img)

        smtp_method = smtplib.SMTP
        if settings.environment == "local":
            smtp_method = smtplib.SMTP_SSL

        with smtp_method(self.host) as smtp:
            if settings.environment == "local":
                smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.send_message(msg_root)
            smtp.quit()
            logger.info("Email sent successfully")

    def __is_active(self) -> bool:
        return not settings.fake_email

    def __log_suggestions(self, body: str):
        logger.info("Suggestions from today:")
        for suggestion in body.split("\n"):
            if not suggestion.strip().startswith("<") and suggestion.strip():
                logger.info(suggestion.strip())
