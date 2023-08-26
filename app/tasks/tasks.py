from celery import Celery
from models import models
from tasks import menuWriter

# celery = Celery('tasks', broker='amqp://localhost:5672')
celery = Celery('tasks', broker='amqp://restaurant_rabbitmq:5672')


@celery.task
def get_xlsx_full_menu(menus_to_file: list[models.Menu]) -> None:
    menuWriter.write(menus_to_file)
