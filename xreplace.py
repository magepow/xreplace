#! /usr/bin/env python3 
# sudo mkdir -p -m 775 /usr/local/bin
# sudo ln -s /Volumes/HOCTAP/GIT/GitHub/xreplace/xreplace.py /usr/local/bin/xreplace
# pip3 install xlrd==1.2.0
# pip3 install pandas
# pip3 install openpyxl
# pip3 install python-dotenv


import os
import sys
from dotenv import load_dotenv
import openpyxl
import pandas as pd
import xml.etree.ElementTree as ET

SCRIPTNAME = __file__
SCRIPT     = os.readlink(SCRIPTNAME);
SCRIPTPATH = os.path.dirname(SCRIPT);
CURRENTDIR = os.getcwd();
FILE_ENV   = '.env'
if not os.path.exists(FILE_ENV) :
    FILE_ENV   = SCRIPTPATH + '/.env'
load_dotenv(FILE_ENV) 
extList    = os.getenv('FILE_EXTENSION').split(' ')
fileRegex = os.getenv('FILE_REGEX')

if len(sys.argv) >= 2 and sys.argv[1] :
    fileRegex = sys.argv[1];

if not os.path.exists(fileRegex) :
   fileRegex   = SCRIPTPATH + '/' + fileRegex

class xreplace:

    def __init__(self):
        if fileRegex.endswith('.xml'):
            self.xreplaceFromXML()
        if fileRegex.endswith('.xlsx'):
            self.xreplaceFromExcel()

    def xreplaceFromXML(self):
        tree = ET.parse(fileRegex)
        root = tree.getroot()
        dataDict  = []
        for item in root:
            findValue    = item.find('find').text
            replaceValue = item.find('replace').text
            dataDict.append({ 'Find': findValue, 'Replace': replaceValue })
        print(dataDict)
        self.findAndReplace(dataDict)

    def xreplaceFromExcel(self):

        xlsx = pd.ExcelFile(fileRegex)
        sheetName = xlsx.sheet_names
        fieldset  = ''
        if 'Find' in sheetName and 'Replace' in sheetName :
            fieldset = 'Sheet'
            findSheet    = xlsx.parse('Find')
            # findData     = findSheet.to_dict('records')
            replaceSheet = xlsx.parse('Replace')
            # replaceData  = replaceSheet.to_dict('records')
            dataframe = pd.concat([findSheet, replaceSheet], axis=1)
            dataDict  = dataframe.to_dict('records')
            self.findAndReplace(dataDict, fieldset)

        if 'Yreplace' in sheetName :
            fieldset  = 'Yreplace'
            dataframe = xlsx.parse('Yreplace', header=None)
            dataList  = dataframe.to_dict('list')
            dataDict  = []
            for item in dataList:
                values  = dataList[item]
                cleanedList = [x for x in values if str(x) != 'nan']
                if len(cleanedList) > 1 :
                    dataDict.append({ 'Find': cleanedList[0], 'Replace': cleanedList[1] })
            self.findAndReplace(dataDict, fieldset)

        if 'Xreplace' in sheetName :
            fieldset = 'Xreplace'
            dataframe = xlsx.parse('Xreplace')
            dataDict = dataframe.to_dict('records')
            self.findAndReplace(dataDict, fieldset)

        if fieldset == '':
            # parse with parame will return frist sheet
            dataframe = xlsx.parse()
            dataDict = dataframe.to_dict('records')
            self.findAndReplace(dataDict)

    def findAndReplace(self, dataDict, fieldset=''):
        # for item in dataDict:
        #     for x in item:
        #         print(f"key: {x}, value: {item[x]}")

        fileList = []
        for root, dirs, files in os.walk(CURRENTDIR):
            for file in files:
                # print(os.path.basename(fileRegex))
                #append the file name to the list
                # print(os.path.join(root,file))
                fileName, fileExt = os.path.splitext(file)
                if fileExt in extList:
                    if file[0] != '.' and file != os.path.basename(fileRegex):
                        fileList.append(os.path.join(root,file))

        totalModified = 0
        for pathFile in fileList :
            with open(pathFile, 'r') as file :
                fileData  = file.read()
                fileData2 = fileData
                for item in dataDict:
                    if pd.isna(item['Find']) == True or pd.isna(item['Replace']) == True:
                        continue
                    fileData2 = fileData2.replace(item['Find'], item['Replace'])

            # Write the file out again
            if fileData != fileData2 :
                with open(pathFile, 'w') as file2:
                    file2.write(fileData2)
                    print(f"File {pathFile} modified!")
                    totalModified = totalModified + 1

        print(f"Total {fieldset} files modified: {totalModified}")

xreplace()
