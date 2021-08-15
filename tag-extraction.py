#import codecs
# html = codecs.open("california-schools.html", 'r').read()

import codecs
import json
from bs4 import BeautifulSoup, NavigableString, Tag

# instantiate local variables
f=codecs.open("california-schools.html", 'r', 'utf-8')
soup=BeautifulSoup(f.read(), 'html.parser')

# create counter of total HS's
hsCounter = 0
highSchools = []

# traverse through all tags on the page
for tag in soup.find_all():

    # determine if this tag is a "UL", we're only interested in UL's
    if "ul" in tag.name:
    
        # traverse through all LI objects
        liTags = tag.find_all('li')
        
        # traverse through all liTags
        for li in liTags:
            
            # traverse through all LI contents
            for content in li.contents:
                
                # check if instance of nav string
                if isinstance(content, NavigableString):
                    
                    # lowercase the string
                    content = content.lower()
                    
                    # only accept string where "High" or "School" or "Public Charter"
                    if "high" in content.lower() or "school" in content.lower() or "public charter" in content.lower():
                        print(content)
                        highSchools.append(content) 
                        hsCounter += 1   
                    else:
                        continue
                        
                if isinstance(content, Tag):
                    
                    # fetch text for link
                    linkTxt = content.getText().lower()
                
                    # determine whether we've found a high school
                    if "high" in linkTxt or "school" in linkTxt:
                        print(linkTxt)
                        highSchools.append(linkTxt) 
                        hsCounter += 1
                    

print("Total Count Of HS's: {}".format(hsCounter))
with open('cali-high-schools.json', 'w') as f:
    json.dump(highSchools, f)

