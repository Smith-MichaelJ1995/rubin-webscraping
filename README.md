Referencing tutorial: https://zenscrape.com/web-scraping-with-python/#:~:text=Advanced%20web%20scraping%20with%20python%3A%20Selenium%201%20a.,a%20browser%20without%20displaying%20the%20graphical%20user%20interface.

# Webscrape Primary Procedure

## Procedure
1. *Phase 0*: Provide keywords & terms as input, links will be generated. 
    - Add links to google document: https://docs.google.com/spreadsheets/d/1QH8TXeyAnptUsh6kvCddxkdQfyfI4ljqlfa231TnJdk/edit#gid=0.
    - Open phantombuster, ensure that google doc link is listed. Configure Phantom to search all records over multiple launches.
    - Set filename as "queryName-state-date".
2. *Phase 1*: 
    - Download JSON output from phantom & place file into "../input" directory.
    - Uncomment Phase1() line & provide the following values:
        - phantomInputJson="<path-of-json-file>"
        - keywords=[<comma-separated-keywords> "Career Technology Education, Vocational Education", "ETC"]
    - Enter 'src' directory & invoke: py index.py
3. *Phase 2*: 
    - Uncomment Phase2()
        - Resolve names & profile links.
    - Enter 'src' directory & invoke: py index.py.
4. *Phase 3*: 
    - Provide path to "../output/persons-of-interest-out-of-network-resolved.json".
    - Uncomment Phase3().