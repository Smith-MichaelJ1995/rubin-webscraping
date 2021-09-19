from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd
import re

def filterLinksForSafeWebpages(links):
    # acceptable webpages
    validLinks = []

    # iterate through all links
    for link in links:

        # I only want links with .org .edu .us in my links, I also must have https
        if (".edu" in link or ".org" in link or ".us" in link) and "https" in link:
            validLinks.append(link)

    # provide valid links back to caller
    return validLinks

def filterLinksForSchoolEmailSuffix(links):
    # acceptable webpages
    validLinks = []

    # iterate through all links
    for link in links:

        # I only want links with .org .edu .us in my links, I also must have https
        if ".edu" in link or ".org" in link or ".us" in link:
            validLinks.append(link)

    # provide valid links back to caller
    return validLinks

# scrape for email address in provided webpage
def fetch_email_addresses_by_webpage(url):

    # determine if email address 

    # initialize webdriver 
    # PATH = "C:\\Users\\micha\\Downloads\\chromedriver_win32\\chromedriver.exe" 
    # driver = webdriver.Chrome(PATH)

    # initialize webdriver - using firefox to limit requests to both browsers.
    profile = webdriver.FirefoxProfile()
    profile.set_preference("http.response.timeout", 10)
    profile.set_preference("dom.max_script_run_time", 10)

    # navigate to web page
    driver = webdriver.Firefox(profile)
    driver.get(url)

    # Getting current URL source code 
    get_source = driver.page_source

    # close the driver, we've captured the data we've needed
    driver.quit()

    # perform regular expression search on email
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", get_source)

    print(emails)
    exit()
    
    return filterLinksForOrgOrEduOrUS(emails)