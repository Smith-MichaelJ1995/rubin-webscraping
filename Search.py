from googlesearch import search
from helpers import fetch_email_addresses_by_webpage, fetch_input_file, write_output_file
import json


class Search:
    def __init__(self):
        
        # District Directory Data Structure: Each Key is a unique district, each Value is a list of unique email addresses belonging to that district.
        self.masterDistrictDirectory = {}

        # Process File, read in all names, return list/dict with all client information
        self.personsListDataFrame = fetch_input_file()


    def write(self):
        print(json.dumps(self.masterDistrictDirectory, indent=4))


    # given the dataframe of admins - generated from .xls file attached, iterate through each person
    # then begin searching for emails
    def run(self):

        # traverse through all search results one by one
        for index, row in self.personsListDataFrame.iterrows():

            # Capture All Email Address Results For This Person
            emailAddressResultsForThisPerson = []

            # Combine School District Name, Faculty Name, Phone # into single searchable text that we'll query via google.
            # Generate Search String Text
            searchStringText = "{}, {}".format(row['InstitutionName'], row['CSO'])
            resultingWebPages = search(searchStringText, num_results=3) 

            # handle case where "searchStringText" is not present in CSO text
            if "NOT AVAILABLE" not in searchStringText:
                searchStringText = "{} Staff Directory".format(row['InstitutionName'])
    

            # CLEARLY INDICATE TO CALLER THAT WE'RE PROCESSING A NEW PERSON
            print()
            print("###########################################################")
            print("PROCESSING NEW INDIVIDUAL: INDEX = {}, PERSON = {}".format(index, row['CSO']))
            print("Total # Web Pages Returned For '{}' = {}".format(searchStringText, len(resultingWebPages)))

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
                
                # traverse all email addresses returned by this webpage
                for emailAddress in emailAddressesForThisWebPage:

                    # extrapolate person from district email domain name
                    person, domain = emailAddress.split("@")

                    # has this perticular email address been identified through results of a previous searchStringText?
                    if self.hasThisEmailAddressBeenReturnedWhenSearchingPreviousPerson(person, domain):
                        print("Igoring Email Address: {}, it has been identified on a prior search for a previous person or 'searchStringText'".format(emailAddress)) 
                    else:
                        self.masterDistrictDirectory[domain].append(emailAddress)
                        print("Unique Email Address Found Related to Search String ({}): {}".format(searchStringText, emailAddress))

            break

    # Given District Directory Data Structure & Provided Email Address, Determine if this new email address should be added to list
    def hasThisEmailAddressBeenReturnedWhenSearchingPreviousPerson(self, person, domain):

        # have we identified this domain before?
        if domain in self.masterDistrictDirectory:

            # traverse through all email addresses identified for this domain
            for previouslyDefinedEmailAddress in self.masterDistrictDirectory[domain]:

                # does this person's email address exist already in the list of emails we've captured for this school district?
                if person.lower() in previouslyDefinedEmailAddress.lower():

                    # inform caller that we should not add this emailAddress to the list
                    return True
            
            # if we've reached this point, then the proposed person has not been identified within the "previouslyDefinedEmailAddress"
            return False

        else:

            # domain has not been identified before, create new entry for it in our masterDistrictDictionary
            self.masterDistrictDirectory[domain] = []
            
            # inform caller that we should add this emailAddress to the list
            return False