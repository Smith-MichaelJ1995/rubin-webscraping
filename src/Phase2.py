import json

class Phase1:
    def __init__(self, path):

        # inform user that we're starting pipeline..
        print("STARTING PHASE 2... Resolve Names For Out-Of-Network Persons")

        # create placeholder for out of network persons (oon) & in-network persons (inn)
        self.results = {
            "oon": [],
            "inn": []
        }

        # convert phantom results to python array object containing dictionaries
        vocational_poi = self.fetch_json_input_file(path)

        # determine persons of interest
        self.is_name_missing_from_poi(vocational_poi)

        # write persons_of_interest data structure to filesystem
        self.write_json_output_file("../current-data/vocational-poi.json", self.results["yes"])
        self.write_json_output_file("../current-data/vocational-non-poi.json", self.results["no"])


    # filter people by out of network/in-network based on existance of 'error' key
    def is_name_missing_from_poi(vocational_poi): 

        # traverse through all people of interest
        for poi in vocational_poi:

            # determine presence of error key
            if "error" in vocational_poi.keys():

                # record that person is out-of-network
                self.results["oon"].append(poi)
            else:
                # record person is in-network
                self.results["inn"].append(poi)

    # fetch phantom results file from system
    def fetch_json_input_file(self, path):
        # fetch file from system
        with open(path, encoding="utf8") as f:
            return json.load(f)

    # write json results to filesystem
    def write_json_output_file(self, path, payload):
        with open(path, "w") as outfile:
            json.dump(payload, outfile, indent=4)


    