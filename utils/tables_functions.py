import openpyxl


def get_table(tables: list[list]) -> str:
    """
        Возвращает путь к файлу таблицы
    """
    wb = openpyxl.Workbook()
    sheet = wb.active

    for row in range(0, len(tables)):
        for column in range(0, 7):
            c1 = sheet.cell(row=row + 1, column=column + 1)
            c1.value = tables[row][column]
    wb.save(f'static.xlsx')
    return f'static.xlsx'