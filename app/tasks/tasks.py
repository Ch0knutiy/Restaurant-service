import xlsxwriter
from celery import Celery

celery = Celery('tasks', broker='amqp://localhost:5672')


@celery.task
def get_xlsx_full_menu():
    workbook = xlsxwriter.Workbook(r'example.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'ID')
    worksheet.write(0, 1, 'Name')
    workbook.close()
