import xlrd, xlwt, re
import csv,datetime
#from sets import Set

def process_file(read_path, write_path):
    """
    Open and read a Excel file
    """
    read_book = xlrd.open_workbook(read_path)
 
    # print number of sheets
    print(read_book.nsheets)
 
    # print sheet names
    print(read_book.sheet_names())
 
    # get the first worksheet
    read_sheet = read_book.sheet_by_name("SAS")
 
    dateSet=[];
    for rownum in range(1, read_sheet.nrows):
        dateTime=datetime.datetime(*xlrd.xldate_as_tuple(read_sheet.cell(rownum,0).value, read_book.datemode))
        dateSet.append(dateTime.date())
    
    
    #write_book=xlwt.Workbook()
    #write_sheet = write_book.add_sheet("Result")
    #write_sheet.write(0, 0, "Company")
    #write_sheet.write(0, 1, "Date")
    # write_sheet.write(0, 2, "Price")
    #write_row=1;
    
    f=open(write_path, 'w', newline='')
    write_book = csv.writer(f, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    write_book.writerow(['Company', 'Date', 'Price'])
    
    for colnum in range(1, read_sheet.ncols):
        company=str(read_sheet.cell(0, colnum).value).strip()
        priceSet=[];
        for rownum in range(1, read_sheet.nrows):
            priceSet.append(str(read_sheet.cell(rownum,colnum).value).strip())
    
        for t_index in range(0, len(dateSet)):
            #write_sheet.write(write_row, 0, company)
            #write_sheet.write(write_row, 1, dateSet[t_index])
            #write_sheet.write(write_row, 2, priceSet[t_index])
            #write_row+=1
            rowInfo=[]
            rowInfo.append(company)
            rowInfo.append(dateSet[t_index])
            rowInfo.append(priceSet[t_index])
            write_book.writerow(rowInfo)
    
    
    f.close()
    #write_book.save(write_path) 





process_file("price.xlsx","price_Result.csv")
print("Finish!")

print("analyze done")