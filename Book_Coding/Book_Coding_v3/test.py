import xlrd, xlwt, re
# from sets import Set

def open_file(excel_path, records, colMapping):
    """
    Open and read a Excel file
    """
    book = xlrd.open_workbook(excel_path)
 
    # print number of sheets
    print(book.nsheets)
 
    # print sheet names
    print(book.sheet_names())
 
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)
 
    for rownum in range(1, first_sheet.nrows):
        tType = str(first_sheet.cell(rownum, colMapping["cType"]).value).strip()
        tYear = int(first_sheet.cell(rownum, colMapping["cYear"]).value)
        tTimes = int(first_sheet.cell(rownum, colMapping["cTimes"]).value)
        #tQCD = int(first_sheet.cell(rownum, colMapping["cQCD"]).value)
        #tQCpublic = int(first_sheet.cell(rownum, colMapping["cQCpublic"]).value)
        #tRestatement = int(first_sheet.cell(rownum, colMapping["cRestatement"]).value)
        #tAuditorName = str(first_sheet.cell(rownum, colMapping["cAuditorName"]).value).strip()
        # print(first_sheet.cell(rownum,colMapping["cObservationCount"]).value)
        tObservationCount = int(first_sheet.cell(rownum, colMapping["cObservationCount"]).value)
        # print(int(tObservationCount))
        tObservations = []
        for tObservationIndex in range(2, tObservationCount + 2):
            tObservations.append(str(first_sheet.cell(rownum, colMapping["cObservationCount"] + tObservationIndex).value).strip())
        
        
        tRecord = Record(tType, tYear, tTimes, tObservations)
        records.append(tRecord)
 


def analyse(records, excel_path):
    """
    statistics and export to a Excel file
    """
    book = xlwt.Workbook()
    
    result_Dic={}
    
    for tRecord in records:
        for tObservation in tRecord.cObservations:
            if tObservation not in result_Dic:
                result_Dic[tObservation]={}            
            if tRecord.cType not in result_Dic[tObservation]:
                result_Dic[tObservation][tRecord.cType]={}
            if tRecord.cTimes not in result_Dic[tObservation][tRecord.cType]:
                result_Dic[tObservation][tRecord.cType][tRecord.cTimes]={}
            if tRecord.cYear not in result_Dic[tObservation][tRecord.cType][tRecord.cTimes]:
                result_Dic[tObservation][tRecord.cType][tRecord.cTimes][tRecord.cYear]=0
            result_Dic[tObservation][tRecord.cType][tRecord.cTimes][tRecord.cYear] = result_Dic[tObservation][tRecord.cType][tRecord.cTimes][tRecord.cYear]+1
                
    
    sheet1 = book.add_sheet("Sum_sum")
    tColNames = ["deficiency", "audit_firm_category", "times", "fyear", "N"]
    tCol = 0
    for tColName in tColNames:
        sheet1.write(0, tCol, tColName)
        tCol = tCol + 1
    
    tRow=1    
    for tDeficiency in result_Dic:
        for tAudit_firm_category in result_Dic[tDeficiency]:
            for tTimes in result_Dic[tDeficiency][tAudit_firm_category]:
                for tYear in result_Dic[tDeficiency][tAudit_firm_category][tTimes]:
                    sheet1.write(tRow, 0, tDeficiency)
                    sheet1.write(tRow, 1, tAudit_firm_category)
                    sheet1.write(tRow, 2, tTimes)
                    sheet1.write(tRow, 3, tYear)
                    sheet1.write(tRow, 4, result_Dic[tDeficiency][tAudit_firm_category][tTimes][tYear])
                    tRow = tRow + 1
        
    
       
    """
    save to excel
    """
    book.save(excel_path) 
    


class Record(object):   
    def __init__(self, cType, cYear, cTimes,cObservations):
        self.cType = cType
        self.cYear = cYear
        self.cTimes = cTimes
        self.cObservations = cObservations



records = [];
colMapping = {"cType":6,
            "cYear":9,
             "cTimes":7,
            "cObservationCount":10}
open_file("Other.xlsx", records, colMapping)
print("Finish!")
analyse(records, "Other_result.xls")
print("analyze done")
