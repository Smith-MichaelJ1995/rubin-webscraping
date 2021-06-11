from googlesearch import search
from helpers import fetch_email_addresses_by_webpage, fetch_input_file, write_output_file
import json


class Search:
    def __init__(self):

        # Process File, read in all names, return list/dict with all client information
        self.personsListDataFrame = fetch_input_file()

        # iterating through all admins, search for contacts and log them
        self.run()

        # write outputs to .xslx
        write_output_file('nys-public-school-admins-with-related-email-contacts.xls', self.personsListDataFrame)


    # given the dataframe of admins - generated from .xls file attached, iterate through each person
    # then begin searching for emails
    def run(self):

        # traverse through all search results one by one
        for index, row in self.personsListDataFrame.iterrows():

            # create placeholder for resulting email address from search
            emailAddressResultForThisPerson = ""

            # extract Institution Name & CSO test fields
            institutionName = row['InstitutionName']
            cso = row['CSO']
            personLastName = cso.split(" ")[-1]

            # Combine School District Name, Faculty Name, Phone # into single searchable text that we'll query via google.
            # Generate Search String Text
            searchStringText = "{}, {}".format(institutionName, cso)
            resultingWebPages = search(searchStringText) 

            # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
            print()
            print("###########################################################")
            print("PROCESSING NEW INDIVIDUAL: INDEX = {}, PERSON = {}".format(index, cso))
            print("Total # Web Pages Returned For '{}' = {}".format(searchStringText, len(resultingWebPages)))

            # handle case where "searchStringText" is not present in CSO text
            if "NOT AVAILABLE" in searchStringText:
                emailAddressResultForThisPerson = "skipping: no name present in CSO text"
            else:

                # iterate through all resulting webpages, pass CSO as that will be used to find person in question 
                emailAddressResultForThisPerson = self.traverse_through_web_pages(resultingWebPages, personLastName)

                # print results to user
                print("Resulting Email Address For Person: {} = {}".format(personLastName, emailAddressResultForThisPerson))

                # record resulting email address, continue processing
                self.personsListDataFrame.at[index, 'RelatedEmailAddresses'] = emailAddressResultForThisPerson
                

    # given web pages returned by search, iterate through them and search for email addresses
    def traverse_through_web_pages(self, resultingWebPages, personLastName):

        # traverse through web pages
        for index, webpage in enumerate(resultingWebPages):

            # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
            print("PROCESSING NEW WEBPAGE: INDEX = {}, URL = {}".format(index, webpage))
            
            # call separate selenium module to gather all email addresses located on this webpage
            emailAddressesForThisWebPage = fetch_email_addresses_by_webpage(webpage)

            # remove duplicates within email address list
            emailAddressesForThisWebPage = list(set(emailAddressesForThisWebPage))

            # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
            print("TOTAL # OF EMAIL ADDRESSES RETURNED FOR THIS WEBPAGE: {}".format(len(emailAddressesForThisWebPage)))

            # search all email addresses, search till we find that of person we're targeting
            personsEmailAddress, found = self.searchEmailsForTargetPerson(emailAddressesForThisWebPage, personLastName)
            
            # halt the traversal if we think we've found this person's email address
            if found == True:
                return personsEmailAddress

        
        # if we made it this far, we didn't find any results and are giving up for this person
        return "No Results Found For Person With Last Name Of: {}".format(personLastName)

    # Given Returned Addresses On This Webpage, decipher of any of them match target person
    # This search isn't perfect: if it encounters another address of another person with the same last name, it will return the address. 
    # This search isn't perfect: If last name isn't spelled exactly in email or abbreviated, it will be missed
    def searchEmailsForTargetPerson(self, emailAddressesForThisWebPage, personLastName):

        # traverse all email addresses returned by this webpage
        for emailAddress in emailAddressesForThisWebPage:

            # determine: is last name within email address?
            if personLastName.lower() in emailAddress.lower():
                return emailAddress, True


        # no results found
        return "", False 
