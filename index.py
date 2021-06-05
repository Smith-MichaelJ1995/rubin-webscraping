from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

# initialize webdriver 
PATH = "C:\\Users\\micha\\Downloads\\chromedriver_win32\\chromedriver.exe" 
driver = webdriver.Chrome(PATH)
 
# navigate to web page 
driver.get("https://www.chufsd.org/Page/666") 

# locate search box 
# search = driver.find_element(with_tag_name("input")) 

# enter search term 
# search.send_keys("staff") 
# search.send_keys(Keys.RETURN) 

try: 
  # locate search results 
  search_results = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "staffdirectorydiv"))) 

  # scrape posts headings 
  facultyList = search_results.find_elements_by_css_selector("div.staff") 

  for faculty in facultyList:
    #   print("faculty = {}".format(faculty.get_attribute('innerHTML'))) 
    name = faculty.find_element_by_css_selector("li.staffname")
    print(name.text)
    # name = faculty.find_elements_by_css_selector("staffname")
    # header = post.find_element_by_tag_name("span")
    # print(name)
  
finally: 
  # quit browser 
  driver.quit()