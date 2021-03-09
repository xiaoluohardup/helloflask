import xlrd
from conf import xlsPath
import numpy as np
from xlrd import xldate_as_tuple
import datetime
class ExcelUtil():
    '''
    返回格式为[(1,2,3),(3,4,5)]
    '''
    def __init__(self, excelPath, sheetIndex=0):
        self.data = xlrd.open_workbook(excelPath)
        self.table = self.data.sheet_by_index(sheetIndex)
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols
        print("表格数据:",self.keys,self.rowNum,self.colNum)

    def dict_data(self):
        list = []
        for row in range(1, self.rowNum):
            print('row',row)
            for col in range(self.colNum):
                value = self.table.cell(row, col).value
                if self.table.cell(row, col).ctype == 3:
                   date = xldate_as_tuple(self.table.cell(row, col).value, 0)
                   value = datetime.datetime(*date)
                   value = str(value)
                list.append(value)
        values = []
        for i in range(0,self.rowNum-1):
            values.append(tuple(list[self.colNum * i: self.colNum * (i+1)]))
        return values

if __name__ == "__main__":
    filepath = xlsPath+'//testsalary.xlsx'
    sheetIndex = 0
    data = ExcelUtil(filepath, sheetIndex).dict_data()
    print('展示表格数据：',data)