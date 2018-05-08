import csv
from pathlib import Path
import http.client
import urllib.parse
import requests
import sys


def read_info_from_csv(file_name, column_index, nrows=None):
    result = []

    file_check = Path(file_name)
    if (not file_check.exists()):
        return result

    with open(file_name, 'r', encoding='utf-8', errors='ignore') as inputFile:
        reader = csv.reader(inputFile)
        next(reader)
        cur_rows = 0
        for row in reader:
            print(cur_rows)
            result.append(row[column_index])
            cur_rows += 1
            if nrows == cur_rows:
                break
    return result


def to_csv(line, file_name, is_append):
    mode = 'w'
    if (is_append == True):
        mode = 'a'
    with open(file_name, mode, newline='') as outputFile:
        writer = csv.writer(outputFile)
        writer.writerow(line)


def unshorten_url(url):
    result = []
    result.append(url)
    last_letter=url[-1]
    if(last_letter.isalpha() or last_letter.isdigit()):
        url=url
    else:
        url=url[:-1]
    try:
        session = requests.Session()  # so connections are recycled
        resp = session.head(url, allow_redirects=True, timeout=90)
        result.append(resp.url)
    except requests.exceptions.RequestException as e:
        result.append(e)
    except:
        result.append(sys.exc_info()[0])
    return result


if __name__ == '__main__':
    output_file_name = "fix_result.csv"
    input_file_name = "fix.csv"
    input_user_infos = read_info_from_csv(input_file_name, 0)
    existing_user_infos_in_output = read_info_from_csv(output_file_name, 0)
    print("-------")
    if (len(existing_user_infos_in_output) <= 0):
        to_csv(["link_short2", "unshort_url"], output_file_name, False)
    total = len(input_user_infos)
    index = len(existing_user_infos_in_output)
    for user_info in input_user_infos:
        # index=index+1
        if user_info in existing_user_infos_in_output:
            continue
        index = index + 1
        print(str(total) + "-" + str(index) + "_" + user_info)
        urlInfo = unshorten_url(user_info)
        to_csv(urlInfo, output_file_name, True)
