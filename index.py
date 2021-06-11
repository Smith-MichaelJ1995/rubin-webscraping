from Search import Search

# instantiate search object, load in administrators data file into DataFrame
search = Search() 

# iterating through all admins, search for contacts and log them
search.run()

# write results to .xslx
search.write()

