#!/usr/bin/env python# encoding: utf-8import csvimport timeimport Levenshteinthreshold_similarity_co_name = 0.8threshold_similarity_people_name = 0.8 # 0.55 the threshold on the distance of two strings, if lower then the two strings are identicaldef name_match(sp1500_file, board_file, output_file_name):        # read file 'input_file_name' to obtain information about the user, such as fullname, twitter account, etc.        sp1500 = [] # information read from sp1500.csv        board = [] # information read from board.csv                with open(sp1500_file) as inputFile :                reader = csv.reader(inputFile)                for row in reader:                        sp1500.append(row)        with open(board_file, encoding='gb18030', errors='ignore') as inputFile :                reader = csv.reader(x.replace('\0', '') for x in inputFile)                for row in reader:                        board.append(row)        output = []        for row in sp1500:                #row = sp1500[row_index, :]                co_per_rol = row[0]                print(co_per_rol)                gvkey = row[1]                cik = row[2]                try:                        cik=int(cik)                except ValueError:                        cik=cik                exec_id = row[3]                exec_full_name = row[9]+" "+row[8]                co_name = row[6]                #year = row[6]                #year = year[2:]                # preprocess exec_full_name                if ", Ph.D." in exec_full_name:                        cut_index = exec_full_name.index(", Ph.D.")                        exec_full_name = exec_full_name[:cut_index]                people_same_company_board = []                # find similar entries in board                # first find similar companies to 'co_name' by 'cik'                for row2 in board:                        individual_name = row2[1]                                                director_id = row2[0]                        company_name_original = row2[6]                        # prune the 'company_name_original' to exclude words in ()s                        index_in_name = -1;                        try:                                index_in_name = company_name_original.index('(');                        except ValueError:                                index_in_name = len(company_name_original)                        company_name = company_name_original[0:index_in_name]                        #print "Company Name:"                        #print company_name                                        company_id = row2[5]                        cik_board= row2[4] #it is cik                        try:                                cik_board = int(cik_board)                        except ValueError:                                cik_board = cik_board                        # if ',' not in row2[4]:                        #                        #         isins.append(row2[4])                        #                        # else:                        #                        #         isins = row2[4].split(", ")                        #print "ISINS:"                        #print isins                                        #print isins                        # individual_role = row2[5]                        #                        # annual_report_year = row2[6]                        #                        # if annual_report_year == "Current":                        #                        #         annual_report_year = "13"                        #                        # else:                        #                        #         annual_report_year = annual_report_year[4:]                        #print "ANNUAL_REPORT_YEAR:"                        #print annual_report_year                                        if cik==cik_board:                                people_same_company_board.append(row2)                        else:                                # print "isins empty"                                similarity_ratio = Levenshtein.ratio(co_name, company_name)                                if similarity_ratio > threshold_similarity_co_name:                                        people_same_company_board.append(row2)                                pass                        # found all people in the same company in board.csv, then match people names                        #print people_same_company_board                for row3 in people_same_company_board:                        #row3 = people_same_company_board[row_index3, :]                        _individual_name = row3[1]                        # prune the individual name                        if "Professor Doctor " in _individual_name:                                _individual_name = _individual_name[17:]                        elif "Professor Dr " in _individual_name:                                _individual_name=_individual_name[13:]                        elif "Professor " in _individual_name:                                _individual_name = _individual_name[10:]                        elif "Doctor " in _individual_name:                                _individual_name = _individual_name[7:]                        elif "Sir " in _individual_name:                                _individual_name=_individual_name[4:]                        elif  "Ambassador " in _individual_name:                                _individual_name=_individual_name[11:]                        _director_id = row3[0]                        _company_id = row3[5]                        _company_name = row3[6]                        _cik = row3[4]                        similarity_ratio = Levenshtein.ratio(exec_full_name, _individual_name)                        _matched = False                        if similarity_ratio > threshold_similarity_people_name:                                #extend the company id and directorId to 'row'                                _matched = True                                row.extend([_director_id, _individual_name, _company_id, _company_name, _cik])                                print(row)                        if _matched is False and similarity_ratio > threshold_similarity_people_name:                                _matched = True                                row.extend([_director_id, _individual_name, _company_id, _company_name, _cik])                                print(row)                        if _matched is True:                                break                output.append(row)        with open(output_file_name, 'w') as outputFile:                writer = csv.writer(outputFile)                write_row_string = ["CO_PER_ROL", "GV_KEY","CIK", "EXEC_ID", "EXEC_FULL_NAME",   "CUSIP","CO_NAME", "permno", "EXEC_LNAME", "EXEC_FNAME", "EXEC_MNAME", "DIRECTOR_ID", "INDIVIDUAL_NAME", "COMPANY_ID", "COMPANY_NAME", "CIK"]                print(write_row_string)                writer.writerow(write_row_string)                writer.writerows(output)if __name__ == '__main__':        output_file_name = "sp1500-new.csv"        input1 = "./sp1500.csv"        input2 = "./board.csv"        print("linking sp1500 and board")        name_match(input1, input2, output_file_name)	