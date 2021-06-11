from googlesearch import search
from webscraper import fetch_email_addresses_by_webpage
import pandas as pd 

# Read in .XSLX file in here
def fetch_input_file():

    # specify path of provided NYS School Admins Directory
    path = "SEDdir.xls"

    # process input file into dataframe
    df = pd.read_excel(path)

    # Must convert column for RelatedEmailAddresses from Float to String
    df['RelatedEmailAddresses'] = df['RelatedEmailAddresses'].astype('string')

    # return dataframe to caller
    return df

# Write DataFrame to 
def write_output_file(df, fileName):

    # convert dict to DataFrame if neccessary
    if type(df) is dict:
        df = pd.DataFrame(data=df, index=[0])

    # create excel writer object
    writer = pd.ExcelWriter(fileName)

    # write dataframe to excel
    df.to_excel(writer)

    # save the excel
    writer.save()

# Given District Directory Data Structure & Provided Email Address, Determine if this new email address should be added to list
def hasThisEmailAddressBeenReturnedWhenSearchingPreviousPerson(masterDistrictDirectory, person, domain):

    print("masterDistrictDirectory = {}".format(masterDistrictDirectory))
    print("type(masterDistrictDirectory) = {}".format(type(masterDistrictDirectory)))
    

    # have we identified this domain before?
    if domain in masterDistrictDirectory:

        # traverse through all email addresses identified for this domain
        for previouslyDefinedEmailAddress in masterDistrictDirectory[domain]:

            # does this person's email address exist already in the list of emails we've captured for this school district?
            if person in previouslyDefinedEmailAddress:

                # inform caller that we should not add this emailAddress to the list
                return True, masterDistrictDirectory
        
        # if we've reached this point, then the proposed person has not been identified within the "previouslyDefinedEmailAddress"
        return False, masterDistrictDirectory

    else:

        # domain has not been identified before, create new entry for it in our masterDistrictDictionary
        masterDistrictDirectory[domain] = []
        
        # inform caller that we should add this emailAddress to the list
        return False, masterDistrictDirectory
        


# District Directory Data Structure: Each Key is a unique district, each Value is a list of unique email addresses belonging to that district.
masterDistrictDirectory = {}

# Process File, read in all names, return list/dict with all client information
personsListDataFrame = fetch_input_file()

# traverse through all search results one by one
for index, row in personsListDataFrame.iterrows():

    # Capture All Email Address Results For This Person
    emailAddressResultsForThisPerson = []

    # Combine School District Name, Faculty Name, Phone # into single searchable text that we'll query via google.
    # Extract InstitutionName & CSO From Current Data Element
    institutionName = row['InstitutionName']
    cso = row['CSO']

    # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
    print()
    print("###########################################################")
    print("PROCESSING NEW INDIVIDUAL: INDEX = {}, PERSON = {}".format(index, cso))

    # Generate Search String Text
    searchStringText = "{}, {}".format(institutionName, cso) 

    # handle case where "searchStringText" is not present in CSO text
    if "NOT AVAILABLE" not in searchStringText:
        searchStringText = "{} Staff Directory".format(institutionName)

    # search web for all pages related to search text
    resultingWebPages = search(searchStringText)

    print("Total # Web Pages Returned For '{}', Size = {}".format(searchStringText, len(resultingWebPages)))

    # traverse through web pages
    for index, webpage in enumerate(resultingWebPages):

        # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
        print("PROCESSING NEW WEBPAGE: INDEX = {}, URL = {}".format(index, webpage))
        
        # call separate selenium module to gather all email addresses located on this webpage
        emailAddressesForThisWebPage = fetch_email_addresses_by_webpage(webpage)

        # remove duplicates within email address list
        emailAddressesForThisWebPage = list(set(emailAddressesForThisWebPage))
        
        # traverse all email addresses returned by this webpage
        for emailAddress in emailAddressesForThisWebPage:

            # has this perticular email address been identified through a previous page we've searched (on this searchStringText)? 
            if emailAddress in emailAddressResultsForThisPerson:
                print("Ignoring Email Address: {}, it has been identified on a prior webpage we found when searching for '{}'".format(emailAddress, searchStringText))
            else:

                # extrapolate district domain name
                person, domain = emailAddress.split("@")

                print("masterDistrictDirectory = {}".format(masterDistrictDirectory))


                masterDistrictDirectory, duplicate = hasThisEmailAddressBeenReturnedWhenSearchingPreviousPerson(masterDistrictDirectory, person, domain)

                # has this perticular email address been identified through results of a previous searchStringText?
                if duplicate:
                    print("Igoring Email Address: {}, it has been identified on a prior search for a previous 'searchStringText'".format(emailAddress)) 
                else:

                    # WE'VE CONFIRMED THAT THIS EMAIL ADDRESS WE'VE FOUND IS UNIQUE: 
                    # Has not been found during searches for prior people or prior webpages on the search for this person 
                    masterDistrictDirectory[domain].append(emailAddress)
                    emailAddressResultsForThisPerson.append(emailAddress)
                    print("Unique Email Address Found Related to Search String ({}): {}".format(searchStringText, emailAddress))

    # print("Resulting Email Addresses For This Person Are: {}".format(emailAddressResultsForThisPerson))
    personsListDataFrame.at[index, 'RelatedEmailAddresses'] = str(emailAddressResultsForThisPerson)

    break

# Script Has Finished Executing, Write Resulting Objects To File
write_output_file(personsListDataFrame, 'nys-public-school-admins-with-related-email-contacts.xls')

# Write Resulting Master Directory Structure to XLS
write_output_file(masterDistrictDirectory, 'nys-public-school-admin-with-related-email-contacts-by-district.xls')


    # print()
    # print("Email Addresses on webpage ({}) = {}".format(facultyPage, emailAddresses))
    # print()
    # this module will query all text strings with the @ symbol, this is most likely the email address of this person we're searching.

    # append this email address to the data model that we've loaded into our script
    
    # REPEAT TILL END OF LIST
        # fetch_link("")
        # res = search("PINE HILLS ELEMENTARY SCHOOL Tia Corniel")