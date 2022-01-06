import pandas as pd
import re
import time
import random
import json
from googlesearch import search
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from helpers import fetch_json_input_file, write_json_output_file, does_field_exist_value_non_null


class Phase4:
    def __init__(self, srcJsonPath, destXlsxPath):

        # Process File, read in all names, return list/dict with all client information
        inputJson = fetch_json_input_file("../output/{}".format(srcJsonPath))

        # Create iterable pd dataframe object
        self.personsListDataFrame = self.build_data_frame(inputJson)

        # iterating through all specified persons, search for contacts and log them
        self.run()

        # write outputs to .xslx
        self.write_output_file_to_xls("../output/{}".format(destXlsxPath), self.personsListDataFrame)

    # Read in vocational-poi.json from path
    def build_data_frame(self, data):

        # convert JSON to Pandas
        pandas_dataframe = pd.json_normalize(data)

        # remove data columns that we don't need
        #pandas_dataframe = pandas_dataframe.drop(['profileUrl', 'fullName', 'firstName', 'lastName', 'profileImageUrl', 
        #    'currentJob', 'pastJob', 'connectionDegree', 'job', 'location', 'url',
        #    'name', 'query', 'category', 'timestamp', 'employer',
        #    'sharedConnections'], axis=1)
            
        # add column for 'email' address
        pandas_dataframe.insert(loc=10, column="email", value="")
            
        # return dataframe to caller
        return pandas_dataframe

    # Write DataFrame to xlsx
    def write_output_file_to_xls(self, fileName, df):

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

            # instantiate search string text as empty to start
            searchStringText = ""

            # extract Institution Name & CSO test fields
            name = row['fullName']
            job = row['currentJob'] if does_field_exist_value_non_null('currentJob', row) else row['job']
            employer = row['employer']
            email = row['email']

            # create placeholder for searchStringText from search
            personLastName = name.split(" ")[-1]

            if index == 10:
               print("Stopping at 10 to validate results")
               break

            # do we have an email address already?
            if "@" not in email: 

                # handle case of employer being "None"
                if employer != "None":

                    # Combine School District Name, Faculty Name into single searchable text that we'll query via google.
                    searchStringText = "{}, {}, Email Address".format(name, employer)

                else:

                    # Combine School District Name, Faculty Name into single searchable text that we'll query via google.
                    searchStringText = "{}, {}, Email Address".format(name, job)

                # CALL FUNCTION: find email suffix based on employer
                # state those within field in this dataframe.
                # CALL FUNCTION: find possible email address matches based on person's last name, letters in first, valid email address suffixes 


                # attempting to handle unforseen error and update data structure on output file
                try:
                    # perform google search
                    resultingWebPages = search(searchStringText, num_results=5)

                    # remove spam or other random crap.. avoiding viruses
                    resultingWebPages = self.filterLinksForSafeWebpages(resultingWebPages) 

                    # handle '-' character in last names
                    if "-" in personLastName:
                        personLastName = personLastName.split("-")[0]

                    # iterate through all resulting webpages, pass name as that will be used to find person in question 
                    # make sure that email address search will be all through lowercases
                    emailAddressResultForThisPerson = self.traverse_through_web_pages(resultingWebPages, personLastName.lower())

                    # print results to user
                    print("Resulting Email Address For Person: {} = {}".format(personLastName, emailAddressResultForThisPerson))

                    # record resulting email address, continue processing
                    self.personsListDataFrame.at[index, 'email'] = emailAddressResultForThisPerson

                    # slow down search too avoid 429 too many requests
                    pauseTime = random.randint(1, 60)
                    print("Sleeping for {} seconds".format(pauseTime))
                    print("")
                    time.sleep(pauseTime)

                except Exception as e:

                    print("")
                    print(e)
                    print("Error has occured.. writing data structure to file")

                    # write outputs to .xslx
                    self.write_output_file('cte-educators-admins.xls', self.personsListDataFrame)
            
            else:

                print("Person: {}, Email Already Found: {}".format(person['fullName'], person['email']))

    # given web pages returned by search, iterate through them and search for email addresses
    def traverse_through_web_pages(self, resultingWebPages, personLastName):

        # valid email address container
        validEmailAddresses = []

        # traverse through web pages
        for index, webpage in enumerate(resultingWebPages):
        
            # call separate selenium module to gather all email addresses located on this webpage
            emailAddressesForThisWebPage = self.fetch_email_addresses_by_webpage(webpage)

            # remove duplicates within email address list
            emailAddressesForThisWebPage = list(set(emailAddressesForThisWebPage))

            # show all email addresses that appear in this search
            #print(emailAddressesForThisWebPage)
            if len(emailAddressesForThisWebPage) > 0:

                # traverse through all email addresses for this web page
                for emailAddress in emailAddressesForThisWebPage:
                    # check if lastname in email address
                    if personLastName.lower() in emailAddress.lower():
                        validEmailAddresses.append(emailAddress.lower())
            
        # remove duplicates via "list(set())" provide results to caller
        return list(set(validEmailAddresses))

            # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
            # print("TOTAL # OF EMAIL ADDRESSES RETURNED FOR THIS WEBPAGE: {}".format(len(emailAddressesForThisWebPage)))

            # search all email addresses, search till we find that of person we're targeting
            #personsEmailAddress, found = self.searchEmailsForTargetPerson(emailAddressesForThisWebPage, personLastName)

            # halt the traversal if we think we've found this person's email address
            #if found == True:
                #return personsEmailAddress

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


    def filterLinksForSafeWebpages(self, links):
        # acceptable webpages
        validLinks = []

        # iterate through all links
        for link in links:

            # I only want links with .org .edu .us in my links, I also must have https
            if (".edu" in link or ".org" in link or ".us" in link) and "https" in link:
                validLinks.append(link)

        # provide valid links back to caller
        return validLinks

    def filterLinksForSchoolEmailSuffix(self, links):
        # acceptable webpages
        validLinks = []

        # iterate through all links
        for link in links:

            # I only want links with .org .edu .us in my links, I also must have https
            if ".edu" in link or ".org" in link or ".us" in link:
                validLinks.append(link)

        # provide valid links back to caller
        return validLinks

    # scrape for email address in provided webpage
    def fetch_email_addresses_by_webpage(self, url):

        # determine if email address 

        # initialize webdriver 
        # PATH = "C:\\Users\\micha\\Downloads\\chromedriver_win32\\chromedriver.exe" 
        # driver = webdriver.Chrome(PATH)

        # initialize webdriver - using firefox to limit requests to both browsers.
        profile = webdriver.FirefoxProfile()
        profile.set_preference("http.response.timeout", 10)
        profile.set_preference("dom.max_script_run_time", 10)

        # navigate to web page
        driver = webdriver.Firefox(profile)
        driver.get(url)

        # Getting current URL source code 
        get_source = driver.page_source

        # close the driver, we've captured the data we've needed
        driver.quit()

        # perform regular expression search on email
        emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", get_source)
        
        return self.filterLinksForSchoolEmailSuffix(emails)