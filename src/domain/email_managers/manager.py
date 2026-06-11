from core.logger import logger
from core.settings import settings
from domain.email_managers.client import SMTPClient
from domain.email_managers.sections.footer import footer
from domain.email_managers.sections.header import header
from domain.email_managers.sections.trends import trends_card
from src.domain.models import Trend


class EmailManager:
    email_title = "Riesgos por vacío de información de hoy"

    def __init__(self) -> None:
        self.client = SMTPClient()

    def send_mail(self, trends: list[Trend]) -> None:
        trends_cards = trends_card(trends)
        body = "".join([header(), trends_cards, footer])
        images = None
        for email in settings.email_list.split("|"):
            self.client.send_mail(self.email_title, body, email, images)
            logger.info(f"Email sent to {email}")
