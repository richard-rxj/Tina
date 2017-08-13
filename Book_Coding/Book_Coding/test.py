import xlrd, xlwt, re
#from sets import Set

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
        tType=str(first_sheet.cell(rownum,colMapping["cType"]).value).strip()
        tYear=int(first_sheet.cell(rownum,colMapping["cYear"]).value)
        tQCD=int(first_sheet.cell(rownum,colMapping["cQCD"]).value)
        tQCpublic=int(first_sheet.cell(rownum,colMapping["cQCpublic"]).value)
        tRestatement=int(first_sheet.cell(rownum,colMapping["cRestatement"]).value)
        tAuditorName=str(first_sheet.cell(rownum,colMapping["cAuditorName"]).value).strip()
        #print(first_sheet.cell(rownum,colMapping["cObservationCount"]).value)
        tObservationCount=int(first_sheet.cell(rownum,colMapping["cObservationCount"]).value)
        #print(int(tObservationCount))
        tObservations=[]
        for tObservationIndex in range(1, tObservationCount+1):
            tObservations.append(str(first_sheet.cell(rownum,colMapping["cObservationCount"]+tObservationIndex).value).strip())
        
        
        tRecord=Record(tType,tYear,tQCD,tQCpublic,tRestatement,tAuditorName,tObservations)
        records.append(tRecord)
 


def analyse(records, observationName, excel_path):
    """
    statistics and export to a Excel file
    """
    book=xlwt.Workbook()
    
    
    """
    count_year
    """
    sheet1 = book.add_sheet("Count_Year")
    sheet1.write(0,0, observationName)
    tCol=1
    for tYear in range(2004, 2016):
        sheet1.write(0,tCol,tYear)
        tCol=tCol+1
    sheet1.write(0, tCol, "total")
 
    
    result_year={};
    for record in records:
        tYear=record.cYear
        tObservations=record.cObservations
         
        for tObservation in tObservations:
            if not result_year.__contains__(tObservation):
                result_year[tObservation]={}
                for tmp in range(2004, 2016):
                    result_year[tObservation][tmp]=0    
                result_year[tObservation]["total"]=0    
            result_year[tObservation][tYear]+=1
            result_year[tObservation]["total"]+=1
 
     
     
    row1=1
     
    for kObservation in result_year.keys():
        sheet1.write(row1,0, kObservation)
        tCol=1;
        for tYear in range(2004, 2016):
            sheet1.write(row1,tCol,result_year[kObservation][tYear])
            tCol=tCol+1
        sheet1.write(row1,tCol,result_year[kObservation]["total"])
        row1+=1
    
    """
    count_type
    """
    sheet1 = book.add_sheet("Count_Type")
    sheet1.write(0,0, observationName)
    tColNames=["big four u.s. auditor","other annually inspected u.s. auditor","triennially inspected u.s. auditor","foreign auditor"]
    tCol=1
    for tColName in tColNames:
        sheet1.write(0,tCol,tColName)
        tCol=tCol+1
    sheet1.write(0, tCol, "total")
 
    
    result={};
    for record in records:
        tName=record.cType
        tObservations=record.cObservations
         
        for tObservation in tObservations:
            if not result.__contains__(tObservation):
                result[tObservation]={}
                for tmp in tColNames:
                    result[tObservation][tmp]=0  
                result[tObservation]["total"]=0       
            if tName in result.get(tObservation):
                result[tObservation][tName]+=1
            result[tObservation]["total"]+=1
     
     
    row1=1
     
    for kObservation in result.keys():
        sheet1.write(row1,0, kObservation)
        tCol=1;
        for tColName in tColNames:
            sheet1.write(row1,tCol,result[kObservation][tColName])
            tCol=tCol+1
        sheet1.write(row1,tCol,result[kObservation]["total"])
        row1+=1
    
    
    """
    count_type  with filter
    """
    tAttrs={"cQCD": [1,0], "cQCpublic": [1,0], "cRestatement": [1,0]}
    for tAttr in tAttrs.keys():
        tfilters=tAttrs[tAttr]
        for tfilter in tfilters:
            sheet1 = book.add_sheet("Count_"+tAttr[1:]+"="+str(tfilter))
            sheet1.write(0,0, observationName)
            tColNames=["big four u.s. auditor","other annually inspected u.s. auditor","triennially inspected u.s. auditor","foreign auditor"]
            tCol=1
            for tColName in tColNames:
                sheet1.write(0,tCol,tColName)
                tCol=tCol+1
            sheet1.write(0, tCol, "total")
         
            
            result={};
            for record in records:
                #print(getattr(record, tAttr))
                if(getattr(record, tAttr)!=tfilter):
                    continue
                tName=record.cType
                tObservations=record.cObservations
                 
                for tObservation in tObservations:
                    if not result.__contains__(tObservation):
                        result[tObservation]={}
                        for tmp in tColNames:
                            result[tObservation][tmp]=0  
                        result[tObservation]["total"]=0       
                    if tName in result.get(tObservation):
                        result[tObservation][tName]+=1
                    result[tObservation]["total"]+=1
             
             
            row1=1
             
            for kObservation in result.keys():
                sheet1.write(row1,0, kObservation)
                tCol=1;
                for tColName in tColNames:
                    sheet1.write(row1,tCol,result[kObservation][tColName])
                    tCol=tCol+1
                sheet1.write(row1,tCol,result[kObservation]["total"])
                row1+=1
    
    
    """
    save to excel
    """
    book.save(excel_path) 
    


class Record(object):   
    def __init__(self, cType, cYear, cQCD, cQCpublic, cRestatement, cAuditorName, cObservations):
        self.cType=cType
        self.cYear = cYear
        self.cQCD=cQCD
        self.cQCpublic = cQCpublic
        self.cRestatement=cRestatement
        self.cAuditorName=cAuditorName
        self.cObservations=cObservations

records=[];
colMapping={"cType":4,
            "cYear":3,
            "cQCD":5,
            "cQCpublic":6,
            "cRestatement":8,
            "cAuditorName":11,
            "cObservationCount":17}
open_file("Book3_coding.xlsx",records, colMapping)
print("Finish!")
analyse(records, "Nature Of Response", "Book3_result.xls")
print("analyze done")