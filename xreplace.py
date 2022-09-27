#! /usr/bin/env python3 
# sudo mkdir -p -m 775 /usr/local/bin
# sudo ln -s /Volumes/HOCTAP/GIT/GitHub/xreplace/xreplace.py /usr/local/bin/xreplace
# pip3 install xlrd==1.2.0
# pip3 install pandas
# pip3 install openpyxl
# pip3 install python-dotenv


import os
from dotenv import load_dotenv
import openpyxl
import pandas as pd

SCRIPTNAME = __file__
SCRIPT     = os.readlink(SCRIPTNAME);
SCRIPTPATH = os.path.dirname(SCRIPT);
CURRENTDIR = os.getcwd();
FILE_ENV   = '.env'
if not os.path.exists(FILE_ENV) :
    FILE_ENV   = SCRIPTPATH + '/.env'
load_dotenv(FILE_ENV) 
extList    = os.getenv('FILE_EXTENSION').split(' ')
regexExcel = os.getenv('FILE_REGEX')
if not os.path.exists(regexExcel) :
   regexExcel   = SCRIPTPATH + '/' + regexExcel

xlsx = pd.ExcelFile(regexExcel)
# print( xlsx.sheet_names)

dataframe = pd.read_excel(regexExcel)
dataDict = dataframe.to_dict('records')

# for item in dataDict:
#     for x in item:
#         print(f"key: {x}, value: {item[x]}")

fileList = []
for root, dirs, files in os.walk(CURRENTDIR):
    for file in files:
        # print(os.path.basename(regexExcel))
        #append the file name to the list
        # print(os.path.join(root,file))
        fileName, fileExt = os.path.splitext(file)
        if fileExt in extList:
            if file[0] != '.' and file != os.path.basename(regexExcel):
                fileList.append(os.path.join(root,file))

totalModified = 0
for pathFile in fileList :
    with open(pathFile, 'r') as file :
        fileData  = file.read()
        fileData2 = fileData
        for item in dataDict:
            fileData2 = fileData2.replace(item['Find'], item['Replace'])

    # Write the file out again
    if fileData != fileData2 :
        with open(pathFile, 'w') as file2:
            file2.write(fileData2)
            print(f"File {pathFile} modified!")
            totalModified = totalModified + 1

print(f"Total files modified: {totalModified}")
