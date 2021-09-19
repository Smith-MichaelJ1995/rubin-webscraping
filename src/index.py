from Phase1 import Phase1
from Phase2 import Phase2
from Phase3 import Phase3

##########
## PHASE 1: Filter For Relevant Persons
##########
#Phase1("../current-data/vocational-educators-directory-admins.json", keywords=["director","vocational"])

##########
## PHASE 2: Resolve Names For Relevant Persons Appearing Out-Of-Network
##########
#Phase2("../current-data/vocational-poi.json")

##########
## PHASE 3: Searching For Emails.. For Each POI having a name/profileLink defined.
##########
Phase3("../current-data/vocational-poi.json")
