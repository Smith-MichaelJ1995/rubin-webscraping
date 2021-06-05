from googlesearch import search
from webscraper import fetch_email_address_by_webpage
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

    # only search when "NAME" is present in CSO text
    if "NOT AVAILABLE" not in searchStringText:

        # grab first link
        res = search(searchStringText)

        # staff page: we're assuming google will give us the faculty page
        facultyPage = res[0]

        # call separate module for selenium to web parse this link
        emailAddresses = fetch_email_address_by_webpage(facultyPage)

        # convert to set such that we can remove dups
        emailAddresses = list(set(emailAddresses))


        print()
        print("Email Addresses on webpage ({}) = {}".format(facultyPage, emailAddresses))
        print()
        # this module will query all text strings with the @ symbol, this is most likely the email address of this person we're searching.

        # append this email address to the data model that we've loaded into our script
    
    # REPEAT TILL END OF LIST
        # fetch_link("")
        # res = search("PINE HILLS ELEMENTARY SCHOOL Tia Corniel")