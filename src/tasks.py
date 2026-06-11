from datetime import datetime, timezone
from time import sleep

from clients.s3_client import get_s3_client
from core.celery_app import celery_app
from core.logger import logger
from core.settings import settings
from domain.delfos_pipeline import DelfosVoidPipeline
from domain.email_managers.manager import EmailManager
from src.clients.external_client import get_external_client
from utils.fake_data import get_fake_metadata, get_fake_trends


@celery_app.task(name="run_delfos_infovoids")
def run_delfos_infovoids(last_ingested_datetime: datetime):
    if last_ingested_datetime.tzinfo is None:
        last_ingested_datetime = last_ingested_datetime.replace(tzinfo=timezone.utc)
    else:
        last_ingested_datetime = last_ingested_datetime.astimezone(timezone.utc)
    logger.info("Running delfos infovoids task")
    # Get clients
    s3_client = get_s3_client()
    external_client = get_external_client()
    email_manager = EmailManager()

    if settings.environment != "local":
        # Run infovoids pipeline
        delfos_voids = DelfosVoidPipeline(last_ingested_datetime)
        delfos_voids.run_workflow()

        # Get results
        voids = delfos_voids.get_trends()
        metadata = delfos_voids.get_metadata()
        email_manager.send_mail(voids)
        last_execution = delfos_voids.state["last_trend_execution"]

    else:
        logger.info("Faking Delfos Execution for local environments")
        sleep(10)
        voids = get_fake_trends()
        metadata = get_fake_metadata()
        last_execution = datetime.now(timezone.utc)

    # Upload results to s3
    path = s3_client.upload_news(voids)
    s3_client.upload_metadata(metadata)

    # Notify External
    external_client.send_info_voids(voids, last_execution, path)

    logger.info(":star: Suggestions task completed!")
