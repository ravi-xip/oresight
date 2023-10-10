import logging

from celery import Celery

from app.database import get_db_session
from entities.website import Website
from repositories.website_repository import WebsiteRepository

app = Celery("tasks")
app.config_from_object("celery_config")


@app.task
def update_website_status(
    website_id: str, status: str, num_prospects: int = -1
) -> Website:
    """
    Triggers a background job to update the status of a website.

    :param website_id: This is the id of the website.
    :param status: This is the status of the website. Possible values are [PROCESSING, INDEXING, COMPLETED, FAILED].
    :param num_prospects: The total number of prospects found for the website.
    :return:
    """
    website_repository = WebsiteRepository(get_db_session())
    website = website_repository.find_by_id(website_id)
    if not website:
        raise ValueError(f"Website with id {website_id} does not exist")

    if status in ["PROCESSING", "INDEXING", "COMPLETED", "FAILED"]:
        website.status = status

    if num_prospects >= 0:
        website.num_prospects = num_prospects

    website = website_repository.update(website)
    logging.debug(f"Updated website: {website.to_dict()}")
    return website
