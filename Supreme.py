import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(r"user-data-dir=C:/Users/raydi/AppData/Local/Google/Chrome/User Data") #Path to your chrome profile
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
prefs = {"profile.default_content_setting_values.geolocation" :2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(executable_path = 'C:\\Users\\raydi\\Driver\\chromedriver.exe',chrome_options=chrome_options)

checkoutUrl = 'https://www.supremenewyork.com/checkout'
# User fills in keyword and color of item
keyword = ''
color1 = ''
color2 = ''
url = 'http://www.supremenewyork.com/shop/all/'


def findItem(keyword, color1, color2):
    keywordFound = False
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    for div in soup.find_all('div', 'turbolink_scroller'):
        for a in div.find_all(href=True):
            if keywordFound:
                if color1 or color2 in a.text:
                    browser.get('http://www.supremenewyork.com' + a['href'])
                    return True #success, breaks operation
                else:
                    color1 = input("Enter color: ")
                    findItem(keyword, color1, color2) #calls the method with new item color
            elif (keyword in a.text): #checks the keyword
                keywordFound = True
            else:
                keywordFound = False


    #parses through the h1 and p tags. h1 for keyword and p for color. The next tag after an h1 is a p(has to be checked again)
    #so the next p after the checked previous h1 will be checked for color and the href will be copied and opened

    return False #assuming the whole url was searched and keyword and color was not found

def checkout(browser):

    # Fills in personal info
    Select(browser.find_element_by_id('order_billing_state')).select_by_visible_text('WA')
    browser.execute_script("document.getElementById('order_billing_name').value = 'Name'")
    browser.execute_script("document.getElementById('order_email').value = 'email@gmail.com'")
    browser.execute_script("document.getElementById('order_tel').value = '123-456-7890'")
    browser.execute_script("document.getElementById('bo').value = 'address'")
    #browser.execute_script("document.getElementById('oba3').value = '325'")
    browser.execute_script("document.getElementById('order_billing_zip').value = '98125'")
    browser.execute_script("document.getElementById('order_billing_city').value = 'Seatle'")

    # Fills in card info
    browser.execute_script("document.getElementById('nnaerb').value = '11111111111111'")
    browser.find_element_by_xpath('//*[@id="orcer"]').send_keys('123')
    browser.execute_script("document.getElementById('credit_card_month').value = '01'")
    browser.execute_script("document.getElementById('credit_card_year').value = '2021'")

    # Checks checkbox and checks out
    browser.execute_script("document.getElementsByClassName('iCheck-helper')[1].click()")
    browser.execute_script("document.getElementsByName('commit')[0].click()")



def main():
    browser.get(url)
    startTime = time.time()
    while(not findItem(keyword,color1,color2)):
        browser.get(url)
        findItem(keyword,color1,color2)

    browser.execute_script("document.getElementsByName('commit')[0].click()") # Clicks on add to cart button

    WebDriverWait(browser,10).until(EC.visibility_of_any_elements_located((By.ID,'cart')))

    browser.execute_script("document.getElementsByClassName('button checkout')[0].click()")

    checkout(browser)

    print("--- %s seconds ---" % (time.time() - startTime)) #timer check

main()
