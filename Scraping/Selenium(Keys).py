from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
driver = webdriver.Firefox()
driver.get("http://www.google.com/")
time.sleep(5)

#open tab
#driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
#body = driver.find_element_by_tag_name('body')
body = driver.find_element_by_css_selector('input#lst-ib.gsfi')

actionChains = ActionChains(driver)

actionChains.context_click(body).perform()

# Load a page
#driver.get('http://stackoverflow.com/')
# Make the tests...

# close the tab
#driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
#driver.close()