import json
import random
import time
from googlesearch import search
from helpers import fetch_json_input_file, write_json_output_file

class Phase2:
    def __init__(self):

        # inform user that we're starting pipeline..
        print("STARTING PHASE 2... Resolve Names For Out-Of-Network Persons")

        # create placeholder for out of network persons (oon) & in-network persons (inn)
        self.records = {
            "oon": [],
            "inn": []
        }

        # fetch people of interest
        vocational_poi = fetch_json_input_file("../output/persons-of-interest.json")

        # determine persons of interest is missing the error key
        self.is_name_missing_from_poi(vocational_poi)

        # traverse through all poi that have the error key
        # resolve out of network link through code.
        #self.fetch_profilelink_for_poi()

        # handle missing persons who could not be resolved
        self.resolve_profilelink_for_unresolved_poi()

        # write persons_of_interest data structure to filesystem
        write_json_output_file("../output/persons-of-interest-out-of-network-resolved.json", self.records["oon"] + self.records["inn"])

    # given unresolvable names from list, resort to setting these fields for each person manually
    def resolve_profilelink_for_unresolved_poi(self):

        # notify user of need to manually set records
        print("Will Need To Resolve The Following Number of OON ppl manually: {}".format(len(self.records["oon"])))

        # traverse through all poi's out-of-network
        for idx, person in enumerate(self.records["oon"]):
        
            # notify user which person we're tracking
            print("processing index: {}".format(idx))

            # create placeholder for position field
            position = ""

            # set position=currentJob by default, if this key is empty, then use job
            # field, subField, obj
            position = does_field_exist_value_non_null('currentJob', 'job', person)

            # create placeholder for search string text
            searchStringText = "{}, Linkedin Profile, {}".format(position, person['location'])

            # set fields based on user input
            print("No Results Found For Search: '{}'".format(searchStringText))
            person['profileUrl'] = input("Profile URL:")
            person['fullName'] = input("Full Name:")

            # remove error key from our dict
            person.pop("error")

            # create additional cursor space
            print("")
    
    # extract profile link url
    def fetch_profilelink_for_poi(self):

        print("Total Persons Of Interest: {}".format(len(self.records["oon"] + self.records["inn"])))
        print("Total Persons Of Interest Out-Of-Network: {}".format(len(self.records["oon"])))

        # traverse through all poi's out-of-network
        for idx, person in enumerate(self.records["oon"]):

            # if idx == 50:
            #     print("quitting.. writing to filesystem")
            #     self.write_json_output_file("../current-data/vocational-poi-names-generated.json", self.records["oon"] + self.records["inn"])
            #     exit()

            #print("processing index: {}".format(idx))

            # blank targetProfileURL & position variable
            targetProfileURL = ""
            position = ""
            links = []

            # set position=currentJob by default, if this key is empty, then use job
            if does_field_exist_value_non_null('currentJob', person):
                position = person['currentJob']
            else:
                position = person['job']

            # create placeholder for search string text
            searchStringText = "{}, Linkedin Profile, {}".format(position, person['location'])

            # perform google search
            try:
                links = search(searchStringText, num_results=5)
            except Exception as e:
                print("The Following Error Has Occured: {}".format(e))
                print("Writing To Filesystem...")
                # write persons_of_interest data structure to filesystem
                self.write_json_output_file("../current-data/vocational-poi-names-generated.json", self.records["oon"] + self.records["inn"])
                exit()
                    
            # handle resulting webpages
            for link in links:

                # determine if a person was returned
                if "/in/" in link:
                    targetProfileURL = link
                    print(targetProfileURL)
                    break
                else:
                    pass
                    #print("passing over non-profile link: {}".format(link))
                    
            # have we found a best-fit profile?
            if targetProfileURL != "":

                # extract name portion of url
                namePortion = targetProfileURL.split("/")[-1]
                        
                # cleansing output for name portion, some names don't have a "-"
                if "-" in namePortion:
                            
                    # extract first/last name
                    firstName, lastName = namePortion.split("-")[0], namePortion.split("-")[1]
                        
                    # update person object, format it with first-letter's capitolized: Michael Smith
                    person['fullName'] = "{} {}".format(firstName[0].upper() + firstName[1:], lastName[0].upper() + lastName[1:])
                        
                else:
                    person['fullName'] = namePortion

                # update target profile url
                person['profileUrl'] = targetProfileURL
                    
                # remove error key from our dict
                person.pop("error")

                # print updated record
                print(person)

            else:
                print("No Results Found For Search: '{}'".format(searchStringText))
                # print("")
                # print("")
                # print("Sorry.. please try for yourself")
                # profileUrl = input("Profile URL:")
                # fullName = input("Full Name:")

                # # does the user want to terminate peacefully here?
                # if profileUrl == "quit" or fullName == "quit":
                #     print("stopping peacefully, not saving any new data for this record...")
                #     return
                # else:

                #     # update profileURL & name
                #     person['profileUrl'] = profileUrl
                #     person['fullName'] = fullName

            # slow down search too avoid 429 too many requests
            pauseTime = random.randint(1, 75)
            print("Sleeping for {} seconds".format(pauseTime))
            print("")
            time.sleep(pauseTime)

            
    
    # filter people by out of network/in-network based on existance of 'error' key
    def is_name_missing_from_poi(self, vocational_poi): 

        # traverse through all people of interest
        for poi in vocational_poi:

            # determine presence of error key
            if "error" in poi.keys():

                # record that person is out-of-network
                self.records["oon"].append(poi)
            else:
                # record person is in-network
                self.records["inn"].append(poi)