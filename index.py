from googlesearch import search
from webscraper import *
import pandas as pd 

# Read in .XSLX file in here
def fetch_input_file():
    path = "SEDdir.xls"
    df = pd.read_excel(path)
    return df

# Process File, read in all names, return list/dict with all client information
personsListDataFrame = fetch_input_file()

# traverse through all search results one by one
for index, row in personsListDataFrame.iterrows():

    # Concatenate test to aide in search accuracy:
    # Combine School District Name, Faculty Name, Phone # into single searchable text that we'll query via google.
    # fetching critical values
    institutionName = row['InstitutionName']
    cso = row['CSO']
    searchStringText = "{}, {}".format(institutionName, cso) 

    # print("Search String Text: {}".format(searchStringText))

        # grab first link

        # call separate module for selenium to web parse this link

        # this module will query all text strings with the @ symbol, this is most likely the email address of this person we're searching.

        # append this email address to the data model that we've loaded into our script
    # REPEAT TILL END OF LIST
        # fetch_link("")
        # res = search("PINE HILLS ELEMENTARY SCHOOL Tia Corniel")