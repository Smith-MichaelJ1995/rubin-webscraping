import json
#from Search import Search
from Filter import filter_relevant_persons

# fetch phantom results file from system
def fetch_input_file(path):

    # fetch file from system
    with open(path, encoding="utf8") as f:
        return json.load(f)

# write json results to filesystem
def write_output_file(path, payload):
    with open(path, "w") as outfile:
        json.dump(payload, outfile, indent=4)

# convert phantom results to python array object containing dictionaries
phantom_search_results = fetch_input_file("../current-data/vocational-educators-directory-admins.json")

# find for persons based on job title
persons_of_interest = filter_relevant_persons(phantom_search_results, keywords=[
        "director", 
        "vocational"
    ]
)

# write persons_of_interest data structure to filesystem
write_output_file("../current-data/vocational-poi.json", persons_of_interest["yes"])
write_output_file("../current-data/vocational-non-poi.json", persons_of_interest["no"])


# instantiate search object, 
# load in administrators data file into DataFrame & perform all steps within constructor
#search = Search() 

