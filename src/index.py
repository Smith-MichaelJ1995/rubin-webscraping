from Phase1 import Phase1
from Phase2 import Phase2

##########
## PHASE 1: Filter For Relevant Persons
##########
#Phase1("../current-data/vocational-educators-directory-admins.json", keywords=["director","vocational"])

##########
## PHASE 2: Resolve Names For Relevant Persons Appearing Out-Of-Network
##########
Phase2("../current-data/vocational-poi.json")


# instantiate search object, 
# load in administrators data file into DataFrame & perform all steps within constructor
#search = Search() 

