import os
import xlrd
import sys
from collections import OrderedDict
import json
import codecs

wb = xlrd.open_workbook('/disk/lulu/T1.xlsx')

convert_list = []
sh = wb.sheet_by_index(0)
title = sh.row_values(0)
dict1 = { }
dict1['N'] = []
for rownum in range(0, sh.nrows):
    rowvalue = sh.row_values(rownum)
    single = OrderedDict()
    for colnum in range(0, len(rowvalue)):
      #  print(rowvalue[colnum])
        single['path'] = rowvalue[colnum]
        dict1['N'].append(single)

    #convert_list.append(dict)

j = json.dumps(dict1)

with codecs.open('file.json', "w", "utf-8") as f:
    f.write(j)
