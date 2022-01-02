import json
from helpers import fetch_json_input_file, write_json_output_file

class Phase1:
    def __init__(self, phantomInputJson, outFile, keywords):

        # inform user that we're starting pipeline..
        print("STARTING PHASE 1... Filter Phantom Results For Persons Of Interest")

        # create placeholder for results variable
        self.results = {
            "yes": [],
            "no": []
        }

        # create placeholder for keywords
        self.keywords = keywords

        # convert phantom results to python array object containing dictionaries
        phantom_search_results = fetch_json_input_file("../input/{}".format(phantomInputJson))

        # determine persons of interest
        self.filter_relevant_persons(phantom_search_results)

        # write persons_of_interest data structure to filesystem
        write_json_output_file("../output/persons-of-interest.json", self.results["yes"])
        write_json_output_file("../output/non-persons-of-interest.json", self.results["no"])

    # given each record in file, determine if individual is a person of interest.
    def filter_relevant_persons(self, data):

        # determine if person of interest
        def determinePersonOfInterest(field, person):
            
            # check "currentJob" field exists on this record
            if len(field) > 0:

                # traverse through all keywords
                for keyword in self.keywords:

                    # determine if keyword exists in field
                    if keyword.lower() in field.lower():

                        # we've identified a person-of-interest by their job title
                        return True

            # no data found indicating that we wan't to persue this person
            return False

        # traverse through each person found in phantom search
        for person in data:

            # flags to determine if we've found a hit
            currentJobFlag = False
            jobFlag = False

            # check currentJob field exists in record; if so, check if person of interest
            if "currentJob" in person.keys():
                currentJobFlag = determinePersonOfInterest(person["currentJob"], person)
            
            # check currentJob field exists in record; if so, check if person of interest
            if "job" in person.keys():
                jobFlag = determinePersonOfInterest(person["job"], person)
            
            
            # if either jobFlag/currentJobFlag of interst, record this record as a yes
            if currentJobFlag or jobFlag:
                self.results["yes"].append(person)
            else:
                self.results["no"].append(person)