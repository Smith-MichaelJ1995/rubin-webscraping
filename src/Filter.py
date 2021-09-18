# given each record in file, determine if individual is a person of interest.
def filter_relevant_persons(data, keywords):

    # determine if person of interest
    def determinePersonOfInterest(field, person):
        
        # check "currentJob" field exists on this record
        if len(field) > 0:

            # traverse through all keywords
            for keyword in keywords:

                # determine if keyword exists in person['currentJob'] field
                if keyword in field.lower():

                    # we've identified a person-of-interest by their job title
                    return True

        # no data found indicating that we wan't to persue this person
        return False

    # create placeholder for resulting data structure
    results = {
        "yes": [],
        "no": []
    }

    # traverse through each person found in phantom search
    for person in data:

        # flag notating if we'd like to persue this person
        currentJobPersonOfInterest = False

        # check currentJob/job field for provided keywords
        if determinePersonOfInterest(person["currentJob"], person) or determinePersonOfInterest(person["job"], person):
            results["yes"].append(person)
        else:
            results["no"].append(person)

    return results