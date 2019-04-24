

import xlsxwriter

def exportToXlsx(outpath, data):
    workbook = xlsxwriter.Workbook(outpath, {'constant_memory': True})
    worksheet = workbook.add_worksheet()

    worksheet.write(1, 0, data['header'])
    for r, row in enumerate(data['lst']):
        for i in range(len(row)):
            worksheet.write(r + 2, i, row[i])

    workbook.close()