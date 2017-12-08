__author__ = 'dag'

import re

from win32com.client import Dispatch


class excel_functions:
    basePath = 'C:\\scripts\\excelwings\\'

    xlApp = None
    xlSheet = None
    workbook = None

    def __init__(self):
        print('Creating excel_functions')

    def openExcel(self, filename):
        print('openExcel', self.basePath + filename)
        self.xlApp = Dispatch('Excel.Application')
        # WARNING: The following line will cause the script to discard any unsaved changes in your workbook
        # Ensure to save any work before running script
        self.xlApp.DisplayAlerts = False

        self.xlApp.ScreenUpdating = True

        self.xlApp.Visible = 1

        self.workbook = self.xlApp.Workbooks.Open(self.basePath + filename)

    def closeExcel(self):
        self.xlApp.ActiveWorkbook.Close()
        # Restore default behaviour
        self.xlApp.DisplayAlerts = True

    def selectSheet(self, sheetname):
        self.xlApp.Sheets(sheetname).Select()
        self.xlSheet = self.xlApp.Sheets(sheetname)

        self.xlSheet.PageSetup.Zoom = 50
        self.xlSheet.PageSetup.FitToPagesTall = 1

    def clearRange(self, inrange):
        print('Clearing range', inrange)
        self.xlSheet.Range(inrange).Select()
        self.xlApp.Selection.ClearContents()

    def getRange(self, inrange):
        # Inrange could be 'A1', 'A1:C5' etc
        return self.xlSheet.Range(inrange)

    def setRange(self, inrange, invalue):
        self.xlSheet.Range(inrange).value = invalue

    def setDataRangeArray(self, startrow, startcol, data_array):
        rows = len(data_array)
        cols = len(data_array[0])
        self.xlSheet.Range(
            self.xlSheet.Cells(startrow, startcol),
            self.xlSheet.Cells(rows + startrow - 1, cols + startcol - 1)).value = data_array

    def exportCharts(self):
        # Exports all the charts in a sheet
        for index, chart in enumerate(self.xlSheet.ChartObjects()):
            currentChart = chart
            currentChart.Activate
            currentChart.Select()
            currentChart.Copy
            filename = r'' + self.basePath + 'charts\\' + str(self.xlSheet.Name) + " " + str(index) + ".png"
            print(filename)
            currentChart.Chart.Export(Filename=filename)

    def exportChartSheet(self, chartname):
        # Export a whole chart sheet
        self.xlApp.Charts(chartname).Select()
        currentChart = self.xlApp.Charts(chartname)
        currentChart.Copy
        filename = r'' + self.basePath + 'charts\\' + str(chartname) + ".png"
        print(filename)
        currentChart.Export(filename)

    def setComboBox(self, comboboxname, invalue):
        item = self.xlSheet.OLEObjects(comboboxname)
        item.Object.value = invalue

    def getComboBox(self, comboboxname):
        item = self.xlSheet.OLEObjects(comboboxname)
        result = item.Object.value
        return result

    def insertImage(self, imgpath, inrange):
        # Inserts an image into the sheet
        rng = self.xlSheet.Range(inrange)
        height = rng.Offset(rng.Rows.Count, 0).Top - rng.Top
        width = rng.Offset(0, rng.Columns.Count).Left - rng.Left
        self.xlSheet.Shapes.AddPicture(imgpath, False, True, rng.Left, rng.Top, height, width)
