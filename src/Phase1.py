import json

class Phase1:
    def __init__(self, path, outFile, keywords):

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
        phantom_search_results = self.fetch_json_input_file(path)

        # determine persons of interest
        self.filter_relevant_persons(phantom_search_results)

        # write persons_of_interest data structure to filesystem
        self.write_json_output_file(outFile, self.results["yes"])
        #self.write_json_output_file("../dest/results/cte-coordinator-non-poi.json", self.results["no"])


    # fetch phantom results file from system
    def fetch_json_input_file(self, path):
        # fetch file from system
        with open(path, encoding="utf8") as f:
            return json.load(f)

    # write json results to filesystem
    def write_json_output_file(self, path, payload):
        with open(path, "w") as outfile:
            json.dump(payload, outfile, indent=4)


    # given each record in file, determine if individual is a person of interest.
    def filter_relevant_persons(self, data):

        # determine if person of interest
        def determinePersonOfInterest(field, person):
            
            # check "currentJob" field exists on this record
            if len(field) > 0:

                # traverse through all keywords
                for keyword in self.keywords:

                    # determine if keyword exists in person['currentJob'] field
                    if keyword.lower() in field.lower():

                        # we've identified a person-of-interest by their job title
                        return True

                # if field is not empty & none of the keywords have been found, then we're not interested in this person
                return False

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