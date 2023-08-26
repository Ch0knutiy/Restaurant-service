import xlsxwriter
from xlsxwriter.worksheet import Worksheet

row = 0
col = 0


def write_dish(dish, worksheet: Worksheet) -> None:
    global row, col
    worksheet.write(row, col + 2, dish['title'])
    worksheet.write(row, col + 3, dish['description'])
    worksheet.write(row, col + 4, dish['price'])
    row += 1


def write_submenu(submenu, worksheet: Worksheet) -> None:
    global row, col
    worksheet.write(row, col + 1, submenu['title'])
    worksheet.write(row, col + 2, submenu['description'])
    row += 1
    for dish in submenu['dishes']:
        write_dish(dish, worksheet)


def write_menu(menu, worksheet: Worksheet) -> None:
    global row, col
    worksheet.write(row, col, menu['title'])
    worksheet.write(row, col + 1, menu['description'])
    row += 1
    for submenu in menu['submenus']:
        write_submenu(submenu, worksheet)


def write(menus) -> None:
    workbook = xlsxwriter.Workbook(r'example.xlsx')
    worksheet = workbook.add_worksheet()
    global row, col
    row, col = 0, 0
    for menu in menus:
        write_menu(menu, worksheet)
    workbook.close()
