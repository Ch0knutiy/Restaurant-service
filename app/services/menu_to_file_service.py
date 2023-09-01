import xlsxwriter
from xlsxwriter.worksheet import Worksheet


class FileWriter:

    def __init__(self):
        self.__row = 0
        self.__col = 0

    def _write_dish(self, dish, worksheet: Worksheet) -> None:
        worksheet.write(self.__row, self.__col + 2, dish['title'])
        worksheet.write(self.__row, self.__col + 3, dish['description'])
        worksheet.write(self.__row, self.__col + 4, dish['price'])
        self.__row += 1

    def _write_submenu(self, submenu, worksheet: Worksheet) -> None:
        worksheet.write(self.__row, self.__col + 1, submenu['title'])
        worksheet.write(self.__row, self.__col + 2, submenu['description'])
        self.__row += 1
        for dish in submenu['dishes']:
            self._write_dish(dish, worksheet)

    def _write_menu(self, menu, worksheet: Worksheet) -> None:
        worksheet.write(self.__row, self.__col, menu['title'])
        worksheet.write(self.__row, self.__col + 1, menu['description'])
        self.__row += 1
        for submenu in menu['submenus']:
            self._write_submenu(submenu, worksheet)

    def write(self, menus) -> None:
        workbook = xlsxwriter.Workbook(r'vol/example.xlsx')
        worksheet = workbook.add_worksheet()
        for menu in menus:
            self._write_menu(menu, worksheet)
        workbook.close()
