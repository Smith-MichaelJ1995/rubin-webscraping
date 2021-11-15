from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd

import openpyxl
from pathlib import Path


class Phase0:

    # build locale spreadsheet from provided file
    def generate_locale_file_from_system(self, path):

        # placeholder for data to be added to the speadsheet
        finalResults = []

        # fetch locale codes from filesystem
        localCodesRawFile = open(path, "r")

        # iterate through all lines in the file
        for line in localCodesRawFile:

            # create columns for: "location", "country", "code"
            rawData = line.split("\t")

            # remove newline character from "code"
            rawData[2] = rawData[2].split("\n")[0]

            # stage record for insertion into spreadsheet
            finalResults.append(rawData)

        # write to spreadsheet
        df = pd.DataFrame(data=finalResults, columns=['Location', 'Country', 'Code'])

        # create excel writer object
        writer = pd.ExcelWriter("location-codes-datatable.xlsx")

        # write dataframe to excel
        df.to_excel(writer)

        # save the excel
        writer.save() 

    def __init__(self):  

        # stage danny's keywords for search
        keywords = [
            "business teacher",
            "marketing teacher",
            "CTAE director",
            "CTE teacher",
            "business professor",
            "marketing professor",
            "entrepreneurship teacher",
            "CTE coordinator"
        ]   

        # fetch location codes file from system, convert into iterable object
        xlsx_file = Path('location-codes-datatable.xlsx')
        wb_obj = openpyxl.load_workbook(xlsx_file)
        sheet = wb_obj.active

        # traverse through all rows in spreadsheet
        for row in sheet.iter_rows(2, sheet.max_row):

            # extract key values from row
            cellLocation = row[1]
            cellCountry = row[2]
            cellCode = row[3]

            # only record of country code is US
            if "United States" in cellLocation.value and cellCountry.value == "US":

                # determine if location code is a state
                if cellLocation.value.count(",") == 1:
                    
                    
                    print(cellLocation.value)


            #print("cellA: {}".format(cellA.value))
            #print("cellLocation: {}".format(cellLocation.value))
            #print("cellCountry: {}".format(cellCountry.value))
            #print("cellCode: {}".format(cellCode.value))

            #exit()
            #for cell in row:
                #print(cell.value)
        

        # signify different states in the US
        # self.locations = [
        #     {
        #       "name": "Alabama, United States, US",
        #       "code": "102240587"
        #     },
        #     {
        #       "name": "Alabama, United States, US",
        #       "code": "102240587"
        #     }
        # ]

        # signify different keywords
        # self.keywords = [

        # ]