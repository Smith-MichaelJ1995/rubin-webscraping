from googlesearch import search
from helpers import fetch_email_addresses_by_webpage, filterLinksForSafeWebpages, filterLinksForSchoolEmailSuffix
import time
import random
import json
import pandas as pd


class Phase4:
    def __init__(self, path):

        # Process File, read in all names, return list/dict with all client information
        self.personsListDataFrame = self.fetch_input_file(path)

        # iterating through all admins, search for contacts and log them
        self.run()

        # write outputs to .xslx
        write_output_file('cte-educators-admins.xls', self.personsListDataFrame)

    # Read in vocational-poi.json from path
    def fetch_input_file(self, path):

        # fetch json from filesystem
        with open(path, encoding="utf8") as f:
            
            # read JSON in from filesystem
            data = json.load(f)
            
            # convert JSON to Pandas
            pandas_dataframe = pd.json_normalize(data)

            # remove data columns that we don't need
            pandas_dataframe = pandas_dataframe.drop(['profileImageUrl','firstName', 'lastName', 'connectionDegree', 'name', 'sharedConnections', 'commonConnection1'], axis=1)
            
            # add column for 'email' address
            pandas_dataframe.insert(loc=10, column="email", value="")
            
            # return dataframe to caller
            return pandas_dataframe

    # Write DataFrame to xlsx
    def write_output_file(self, fileName, df):

        # create excel writer object
        writer = pd.ExcelWriter(fileName)

        # write dataframe to excel
        df.to_excel(writer)

        # save the excel
        writer.save()

    # find viable email suffixes for district/school
    # def fetch_email_suffix(self):

        # build search string text for webpages: search "employer & email info"

        # filter results to contain only .edu/.org/.us/https

        # open each webpage
            
            # search for an "@", capture all email addresses

            # filter those emails to only contain values .edu/.org/.us 

            # if length of result > 0, then stop & return values list 

        # inform runner that no valid prefixes found for this district/school, return None

    # find email address given person's name
    # def find_email_address_for_person(self):   

        # handle splitting person's last name

        # build search string text for persons: search "person name, employer, email address"
        # MAYBE TRY DIFFERENT SEARCH QUERY COMBOS? 

        # filter resulting links to only contain .edu/.org/.us

        # for each page/resulting links

            # open page, fetch all possible email addresses

            # for each email address found

                # check if person's last name in email prefix section (before the "@")

                    # check if first letter of person's first name exists in splitted array (split email prefix section based on person's last name)

                # check if email suffix section within list of approved email suffixes for this record

                


    # given the dataframe of admins - generated from .xls file attached, iterate through each person
    # then begin searching for emails
    def run(self):

        # traverse through all search results one by one
        for index, row in self.personsListDataFrame.iterrows(): 

            # extract Institution Name & CSO test fields
            name = row['fullName']
            job = row['currentJob'] if len(row['currentJob']) > 0 else row['job']
            employer = row['employer']
            email = row['email']

            # create placeholder for searchStringText from search
            personLastName = name.split(" ")[-1] 

            # Combine School District Name, Faculty Name, Phone # into single searchable text that we'll query via google.
            searchStringText = "{}, Email Information".format(name)

            # do we have an email address already?
            if "@" in email:

                # CALL FUNCTION: find email suffix based on employer
                # state those within field in this dataframe.


                # CALL FUNCTION: find possible email address matches based on person's last name, letters in first, valid email address suffixes 


                # attempting to handle unforseen error and update data structure on output file
                try:
                    # perform google search
                    resultingWebPages = search(searchStringText, num_results=7)

                    # remove spam or other random crap.. avoiding viruses
                    resultingWebPages = filterLinksForSafeWebpages(resultingWebPages) 

                    # handle '-' character in last names
                    if "-" in personLastName:
                        personLastName = personLastName.split("-")[0]

                    # iterate through all resulting webpages, pass CSO as that will be used to find person in question 
                    emailAddressResultForThisPerson = self.traverse_through_web_pages(resultingWebPages, personLastName)

                    # print results to user
                    print("Resulting Email Address For District: {} = {}".format(personLastName, emailAddressResultForThisPerson))
                    exit()

                    # record resulting email address, continue processing
                    self.personsListDataFrame.at[index, 'Email'] = emailAddressResultForThisPerson

                    # slow down search too avoid 429 too many requests
                    pauseTime = random.randint(1, 45)
                    print("Sleeping for {} seconds".format(pauseTime))
                    print("")
                    time.sleep(pauseTime)

                except Exception as e:

                    print("")
                    print(e)
                    print("Error has occured.. writing data structure to file")

                    # write outputs to .xslx
                    write_output_file('cte-educators-admins.xls', self.personsListDataFrame)
            
            else:

                print("Person: {}, Email Already Found: {}".format(name, email))

    # given web pages returned by search, iterate through them and search for email addresses
    def traverse_through_web_pages(self, resultingWebPages, personLastName):

        # traverse through web pages
        for index, webpage in enumerate(resultingWebPages):
        
            # call separate selenium module to gather all email addresses located on this webpage
            emailAddressesForThisWebPage = fetch_email_addresses_by_webpage(webpage)

            # remove duplicates within email address list
            emailAddressesForThisWebPage = list(set(emailAddressesForThisWebPage))

            # show all email addresses that appear in this search
            #print(emailAddressesForThisWebPage)
            if len(emailAddressesForThisWebPage) > 0:
                return emailAddressesForThisWebPage
            

            # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
            # print("TOTAL # OF EMAIL ADDRESSES RETURNED FOR THIS WEBPAGE: {}".format(len(emailAddressesForThisWebPage)))

            # search all email addresses, search till we find that of person we're targeting
            #personsEmailAddress, found = self.searchEmailsForTargetPerson(emailAddressesForThisWebPage, personLastName)

            # halt the traversal if we think we've found this person's email address
            #if found == True:
                #return personsEmailAddress

        
        # if we made it this far, we didn't find any results and are giving up for this person
        # return "None"

    # Given Returned Addresses On This Webpage, decipher of any of them match target person
    # This search isn't perfect: if it encounters another address of another person with the same last name, it will return the address. 
    # This search isn't perfect: If last name isn't spelled exactly in email or abbreviated, it will be missed
    def searchEmailsForTargetPerson(self, emailAddressesForThisWebPage, personLastName):

        # handle the irish last name cases: o'shea, o'connor, o'brien.. need to remove "'" character
        if "'" in personLastName:
            personLastName = personLastName.replace("'",'')

        # traverse all email addresses returned by this webpage
        for emailAddress in emailAddressesForThisWebPage:

            # determine: is last name within email address?
            if personLastName.lower() in emailAddress.lower():
                return emailAddress, True


        # no results found
        return "", False 

    