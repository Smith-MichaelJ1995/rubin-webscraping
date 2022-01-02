import time
import random
import json
import pandas as pd
from googlesearch import search
from helpers import fetch_json_input_file, write_json_output_file


class Phase3:
    def __init__(self, path):

        # inform user that we're starting pipeline..
        print("STARTING PHASE 3... Resolve Employer For Educating Director")

        # Process File, read in all names, return list/dict with all client information
        self.records = fetch_json_input_file("../output/persons-of-interest-out-of-network-resolved.json")

        # iterating through all admins, search for contacts and log them
        self.run()

        # write outputs to json
        write_json_output_file("../output/persons-of-interest-oon-resolved-with-employers", self.records)

    # given the dataframe of admins - generated from .xls file attached, iterate through each person
    # then begin searching for emails
    def run(self):

        # traverse through all poi's out-of-network
        for idx, person in enumerate(self.records):

            # create placeholder for position of person
            position = ""
            separator = "at "

            # calculate employer based on "at" string in currentJob/job field
            if len(person['currentJob']) > 0 and separator in person['currentJob']:
                position = person['currentJob'].split(separator)[-1]
            elif len(person['job']) > 0 and separator in person['job']:
                position = person['job'].split(separator)[-1]
            else:
                position = "None"

            # set person's employer field equal to the position we've derived in step above
            person['employer'] = position



        
     

    