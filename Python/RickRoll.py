import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/Jack/AppData/Local/Google/Chrome/User Data/")
options.add_argument("--profile-directory=Profile 1")
driver = webdriver.Chrome(PATH, options=options)


driver.get("https://www.youtube.com")

YoutubeSearch = driver.find_element(By.NAME, "search_query")
YoutubeSearch.click()
YoutubeSearch.send_keys("Never Gonna Give You Up")
YoutubeSearch.send_keys(Keys.RETURN)

time.sleep(3)

Rick = driver.find_element(By.XPATH, "//*[@title='Rick Astley - Never Gonna Give You Up (Official Music Video)']")
Rick.click()

print("You just got Rick Rolled")

time.sleep(70)

driver.quit()