from googlesearch import search
from helpers import fetch_email_addresses_by_webpage, filterLinksForSafeWebpages, filterLinksForSchoolEmailSuffix
import time
import random
import json
import pandas as pd


class Phase3:
    def __init__(self, path):

        # Process File, read in all names, return list/dict with all client information
        self.personsListDataFrame = self.fetch_json_input_file(path)

        # iterating through all admins, search for contacts and log them
        self.run()

        # write outputs to .xslx
        write_output_file('cte-educators-admins.xls', self.personsListDataFrame)

    # Read in vocational-poi.json from path
    def fetch_json_input_file(self, path):
        with open(path, encoding="utf8") as f:
            return json.load(f)

    # write json results to filesystem
    def write_json_output_file(self, path, payload):
        with open(path, "w") as outfile:
            json.dump(payload, outfile, indent=4)

    # given the dataframe of admins - generated from .xls file attached, iterate through each person
    # then begin searching for emails
    def run(self):

        
     

    