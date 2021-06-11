from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd
import re

# scrape for email address in provided webpage
def fetch_email_addresses_by_webpage(url):

    # initialize webdriver 
    PATH = "C:\\Users\\micha\\Downloads\\chromedriver_win32\\chromedriver.exe" 
    driver = webdriver.Chrome(PATH)
    
    # navigate to web page 
    driver.get(url) 

    # Getting current URL source code 
    get_source = driver.page_source

    # perform regular expression search on email
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", get_source)
    
    return emails


# Read in .XSLX file in here
def fetch_input_file():

    # specify path of provided NYS School Admins Directory
    path = "SEDdir.xls"

    # process input file into dataframe
    df = pd.read_excel(path)

    # Must convert column for RelatedEmailAddresses from Float to String
    df['RelatedEmailAddresses'] = df['RelatedEmailAddresses'].astype('string')

    # return dataframe to caller
    return df

# Write DataFrame to 
def write_output_file(fileName):

    # convert dict to DataFrame if neccessary
    if type(df) is dict:
        df = pd.DataFrame(data=df, index=[0])

    # create excel writer object
    writer = pd.ExcelWriter(fileName)

    # write dataframe to excel
    df.to_excel(writer)

    # save the excel
    writer.save()