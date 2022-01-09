Referencing tutorial: https://zenscrape.com/web-scraping-with-python/#:~:text=Advanced%20web%20scraping%20with%20python%3A%20Selenium%201%20a.,a%20browser%20without%20displaying%20the%20graphical%20user%20interface.

# Webscrape Primary Procedure

## Procedure
1. *Phase0.py*: (Generating links to be searched on LinkedIn through phantombuster).
    - Procedure:
        - Uncomment the following line on index.py: 
            Phase0(keywords = [
                "business teacher",
                "marketing teacher",
                "CTAE director",
                "CTE teacher",
                "business professor",
                "marketing professor",
                "entrepreneurship teacher",
                "CTE coordinator"
            ])
        - Replace with keywords that you'd like to search for.
        - Invoke script:
            - ```cd src & py index.py```
        - All LinkedIn query search links will be written the following folder: "../output/linkedin-query-links.xlsx"
        - Copy links to google document: https://docs.google.com/spreadsheets/d/1QH8TXeyAnptUsh6kvCddxkdQfyfI4ljqlfa231TnJdk/edit#gid=0.
        - Open Phantombuster, ensure that google doc link is listed within google sheets text box. Configure Phantom to search all records over multiple launches.
        - Im Phantombuster, set output filename as "queryName-state-date".
2. *Phase1.py* (Given Phantombuster JSON search output, determine people of interest by providing sub-terms to identify within the profile): 
    - Invoke phantombuster search. When finished, download JSON output from phantom & place file into "../input" directory.
    - At this point in time, run the 'webscape-backend' script (within webscrape-backend repo) to determine which records are truly unique, Should operate on database.xls.
    - Uncomment Phase1() line & provide the following values:
        - phantomInputJson="<path-of-json-file>"
        - keywords=[<comma-separated-keywords> "Career Technology Education, Vocational Education", etc]
    - Invoke script:
        - ```cd src & py index.py```
    - Output will be written to:
        - ```../output/persons-of-interest.json```
3. *Phase2.py* (Given the 'of-interest' people that are out-of-network, resolves names & profileURL links.): 
    - Uncomment Phase2()
    - Invoke script:
        - ```cd src & py index.py```
    - Output will be written to:
        - ```"../output/persons-of-interest-out-of-network-resolved.json"```
4. *Phase3.py* (Given remaining persons.. determine 'employer' from 'job' field & stage value into column for each record.): 
    - Provide path to "../output/persons-of-interest-out-of-network-resolved.json".
    - Uncomment Phase3(path="../output/persons-of-interest-out-of-network-resolved.json").
    - Invoke script:
        - ```cd src & py index.py```
    - Output will be written to:
        - ```../output/persons-of-interest-oon-resolved-with-employers```
5. *Phase4.py* (Given remaining persons we're interested in, attempt to query for email addresses): 
    - Uncomment Phase4().
        - Path towards "../../webscraping-backend/data/database.xls" is defined in class.
    - Invoke script:
        - ```cd src & py index.py```
    - Output will be written to:
        - ```../output/email-query-output.xls```
