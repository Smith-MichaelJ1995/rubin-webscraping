# import modules for all four phases
from Phase0 import Phase0
from Phase1 import Phase1
from Phase2 import Phase2
from Phase3 import Phase3
from Phase4 import Phase4

##########
## PHASE 0:
##########
#Phase0()


##########
## PHASE 1: Filter For Relevant Persons
##########
# PASSED TERM: "business-professor" -- 0
# PASSED TERM: "ctae-director" -- 0
# PASSED TERM: "entreprenuership-teacher" -- 0
# PASSED TERM: "marketing-professor" -- 0
# TERM: "cte-coordinator" -- 12 
# TERM: "business-teacher" -- 2
# TERM: "cte-teacher" -- 12
# TERM: "marketing-teacher" -- 1

# Phase1(
#     "../data/json/new-york-state-cte-teacher.json",
#     "../data/json/results/cte-teacher.json",
#     keywords=["Career & Technical Education", "Career and Technical Education", "CTE", "Career & Technology Education", "Career and Technology Education", "Technology Education"]
# )

##########
## PHASE 2: Resolve Names For Relevant Persons Appearing Out-Of-Network
##########
# Phase2("../current-data/vocational-poi.json")

##########
## PHASE 3: Compute Employers For People Of Interest
##########
# Phase3("../data/json/results/new-york-state-cte-results-11-21-2021.json")

##########
## PHASE 4: Searching For Emails.. For Each POI having a name/profileLink defined.
##########
Phase4(
    inputPath="../data/json/results/new-york-state-cte-results-11-21-2021.json",
    outputPath="../data/xls/new-york-state-cte-results-11-21-2021.xls"
)
