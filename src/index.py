# import modules for all four phases
from Phase1 import Phase1
from Phase2 import Phase2
from Phase3 import Phase3
from Phase4 import Phase4

##########
## PHASE 1: Filter For Relevant Persons
##########
#Phase1("../script-input/new-york-state-cte-12-30-2021.json", keywords=["CTE","director","coordinator"])

##########
## PHASE 2: Resolve Names For Relevant Persons Appearing Out-Of-Network
##########
#Phase2("../script-output/cte-poi.json")

##########
## PHASE 3: Compute Employers For People Of Interest
##########
#Phase3("../current-data/vocational-poi.json")

##########
## PHASE 4: Searching For Emails.. For Each POI having a name/profileLink defined.
##########
Phase4(srcJsonPath = "../script-output/cte-poi-names-generated.json", destXlsxPath = "../script-output/cte-poi-names-generated.xls")
