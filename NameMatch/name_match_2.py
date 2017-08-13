#!/usr/bin/env python
# encoding: utf-8
import csv
import time
import Levenshtein

threshold_similarity_co_name = 0.7
#threshold_similarity_people_name = 0.6 # 0.55 the threshold on the distance of two strings, if lower then the two strings are identical

def name_match(match_file1, match_file2, output_file_name, colume_name):

        # read file 'input_file_name' to obtain information about the user, such as fullname, twitter account, etc.

        match_dataset1 = [] # information read from match_dataset1.csv
        match_dataset2 = [] # information read from match_dataset2.csv

        first_row = True
        with open(match_file1, 'r') as inputFile :
                reader = csv.reader(inputFile)
                for row in reader:
                        if first_row:
                                first_row = False
                                continue
                        match_dataset1.append(row)
        
        first_row = True
        with open(match_file2, 'r') as inputFile :
                reader = csv.reader(inputFile)
                for row in reader:
                        if first_row:
                                first_row = False
                                continue
                        match_dataset2.append(row)

        output = []
        for row in match_dataset1:
                #row = match_dataset1[row_index, :]
                asx_code = row[0]
                company_name = row[1]
                print (row)

                matched = None
                for row2 in match_dataset2:
                        controllering_corproation = row2[0]
                        similarity_ratio = Levenshtein.ratio(company_name, controllering_corproation)
                        if similarity_ratio > threshold_similarity_co_name:
                                matched = True
                                print ("matched")
                                row.append(controllering_corproation)
                                output.append(row)
                                break
                        pass
                if not matched:
                        row.append("-")
                        output.append(row)
                
        with open(output_file_name, 'w', newline='') as outputFile:
                writer = csv.writer(outputFile)
                write_row_string = ["ASX code", "Controlled entities"]
                write_row_string.extend(colume_name)
                print (write_row_string)                writer.writerow(write_row_string)
                writer.writerows(output)

if __name__ == '__main__':                output_file_name = "./DataMatched0.csv"        input1 = "./DataMatched.csv"        input2 = "./Data_2014_2015.csv"        colume_names = ["Match with 2014_2015"]        name_match(input1, input2, output_file_name, colume_names)                
        output_file_name = "./DataMatched1.csv"
        input1 = "./DataMatched0.csv"
        input2 = "./Data_2013_2014.csv"
        colume_names = ["Match with 2014_2015", "Match with 2013_2014"]
        name_match(input1, input2, output_file_name, colume_names)

        output_file_name = "./DataMatched2.csv"
        input1 = "./DataMatched1.csv"
        input2 = "./Data_2012_2013.csv"
        colume_names = ["Match with 2014_2015", "Match with 2013_2014", "Match with 2012_2013"]
        name_match(input1, input2, output_file_name, colume_names)
        

        output_file_name = "./DataMatched3.csv"
        input1 = "./DataMatched2.csv"
        input2 = "./Data_2011_2012.csv"
        colume_names = ["Match with 2014_2015", "Match with 2013_2014", "Match with 2012_2013", "Match with 2011_2012"]
        name_match(input1, input2, output_file_name, colume_names)

        output_file_name = "./DataMatched4.csv"
        input1 = "./DataMatched3.csv"
        input2 = "./Data_2010_2011.csv"
        colume_names = ["Match with 2014_2015", "Match with 2013_2014", "Match with 2012_2013", "Match with 2011_2012", "Match with 2010_2011"]
        name_match(input1, input2, output_file_name, colume_names)

        output_file_name = "./DataMatched5.csv"
        input1 = "./DataMatched4.csv"
        input2 = "./Data_2009_2010.csv"
        colume_names = ["Match with 2014_2015", "Match with 2013_2014", "Match with 2012_2013", "Match with 2011_2012", "Match with 2010_2011", "Match with 2009_2010"]
        name_match(input1, input2, output_file_name, colume_names)
        
        output_file_name = "./DataMatched6.csv"
        input1 = "./DataMatched5.csv"
        input2 = "./Data_2008_2009.csv"
        colume_names = ["Match with 2014_2015", "Match with 2013_2014", "Match with 2012_2013", "Match with 2011_2012", "Match with 2010_2011", "Match with 2009_2010", "Match with 2008_2009"]
        name_match(input1, input2, output_file_name, colume_names)        print (threshold_similarity_co_name)
