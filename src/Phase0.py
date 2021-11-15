from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd


class Phase0:

    # Write DataFrame to xlsx
    def write_output_file(self, fileName, df):

        # create excel writer object
        writer = pd.ExcelWriter(fileName)

        # write dataframe to excel
        df.to_excel(writer)

        # save the excel
        writer.save()

    def __init__(self):

        # placeholder for data to be added to the speadsheet
        finalResults = []

        # fetch locale codes from filesystem
        localCodesRawFile = open("../linkedin-location-codes.txt", "r")

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