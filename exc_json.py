from __future__ import unicode_literals
import xlrd
import json
import os
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
cols = []

def achieve_data(file_path):
    try:
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print("Excel loads unsuccessful! - %s" % file_path)
        return None

def excel2json(excfile,sheet_index,jsfile):
    data = achieve_data(excfile)
    if data is not None:
        # get sheet name
        worksheets = data.sheet_names()
        print("sheets index and name:")
        for index, sheet in enumerate(worksheets):
            print(index, sheet)
        table = data.sheet_by_index(sheet_index)
        # get sheet title
        titles = table.row_values(0)
        result = []
        #write data
        for i in range(1, table.nrows):
            print('Writing line %s...' % i)
            row = table.row_values(i)
            tmp = {}
            for index, title in enumerate(titles):
                # split '|' to list
                if '|' in row[index]:
                    tmp[title] = row[index].split('|')
                #ignore null
                elif row[index] == '':
                    pass
                else:
                    tmp[title] = row[index]
            result.append(tmp)
        with open(jsfile, 'w', encoding='utf-8') as f:
            print('Saving...')
            f.write(json.dumps(result,ensure_ascii=False))
            print('Excel to json successful!')

def json2excel(jsfile, excfile, title):
    # read title
    ws.title = title
    a = 1
    if os.path.exists(jsfile):
        # write column name
        with open(jsfile, 'r',encoding='utf8') as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                else:
                    # load data
                    jsdata = json.loads(line)
                    # key to title
                    for k in jsdata.keys():
                        if k not in cols:
                            cols.append(k)
            ws.append(cols)
        # write value
        with open(jsfile, 'r', encoding='utf8') as fp:
                while True:
                    #use break when data is too large
                    if a >= 1000:
                        break
                    line = fp.readline()
                    #end writing
                    if not line:
                        break
                    print('Writing line %s...' % a)
                    jsdata = json.loads(line)
                    rowdata = []
                    for col in cols:
                        if col in jsdata.keys():
                            if isinstance(jsdata.get(col), list):
                                rowdata.append("|".join(jsdata.get(col)))
                            else:
                                rowdata.append(str(jsdata.get(col)))
                    a += 1
                    ws.append(rowdata) # Write lines
    print('Saving...')
    wb.save(excfile)
    print('Json to excel successful!')

if __name__ == '__main__':
    jsfile_in = './data/medical.json'
    jsfile = './data/test_large.json'
    excfile = './data/data.xlsx'
    sheet_index = 0
    json2excel(jsfile_in,excfile,'data')
    excel2json(excfile, sheet_index, jsfile)