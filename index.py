from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

# initialize webdriver 
PATH = "C:\\Users\\micha\\Downloads\\chromedriver_win32\\chromedriver.exe" 
driver = webdriver.Chrome(PATH)
 
# navigate to web page 
driver.get("https://www.reddit.com/") 

# locate search box 
search = driver.find_element_by_name("q") 

# enter search term 
search.send_keys("scraping") 
search.send_keys(Keys.RETURN) 

try: 
  # locate search results 
  search_results = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "rpBJOHq2PR60pnwJlUyP0"))) 

  # scrape posts headings 
  posts = search_results.find_elements_by_css_selector("h3._eYtD2XCVieq6emjKBH3m") 

  for post in posts: 
    header = post.find_element_by_tag_name("span")
    print(header.text)
  
finally: 
  # quit browser 
  driver.quit()