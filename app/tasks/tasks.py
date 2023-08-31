import asyncio

from celery import Celery
from models import models
from services.menu_to_file_service import FileWriter

# celery = Celery('tasks', broker='amqp://localhost:5672')
celery = Celery('tasks', broker='amqp://restaurant_rabbitmq:5672')
loop = asyncio.get_event_loop()


@celery.task
def get_xlsx_full_menu(menus_to_file: list[models.Menu]) -> None:
    writer = FileWriter()
    writer.write(menus_to_file)
