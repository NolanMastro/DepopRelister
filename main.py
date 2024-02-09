import random
import time
import os
import requests
import shutil
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

global clear
clear = lambda: os.system('clear')
load_dotenv()


def login(EMAIL, PASSWORD, driver):
    clear()
    print(f'Status: Logging into {username}')
    driver.get("https://www.depop.com/login/")
    time.sleep(0.2)
    try:
        #accept cookies
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/button[2]').click()
    except:
        print("Failed to click accept cookies.")
    try:
        #enter username and password fields
        driver.find_element(By.ID, 'username').send_keys(EMAIL)
        time.sleep(random.randint(0,1))
        driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    except:
        try:
            #wait for page to load.
            username_field = driver.find_element(By.ID, value='username')
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(username_field)
            )
            username_field.send_keys(EMAIL)
            driver.find_element(By.ID, 'password').send_keys(PASSWORD)
        except:
            print("Failed sign in, goodbye.")
    #click login button
    driver.find_element(By.CSS_SELECTOR, '#main > div:nth-child(6) > form > button').click()
    time.sleep(5)

def relist(driver):
    driver.get('https://www.depop.com/sellinghub/selling/')
    time.sleep(5)
    elem = driver.find_element(By.CSS_SELECTOR, '#__next > div > div > div > div.SellerHubLayout-styles__SellerHubChildrenWrapper-sc-80d6b1bd-1.fXfKUa > div > h2').text.strip()
    global listingCount
    listingCount = ''
    for char in elem:
        if char.isdigit():
            listingCount += char 
    listingCount = int(listingCount)
    print(f'{listingCount} active listings. ETA: {round(listingCount * 55/60)} min.')
    driver.get(f'https://depop.com/{username}')
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '#main > div.Container-sc-21c8a640-0.ShopNavigation-styles__Wrapper-sc-b599f1d4-0.fagice.eNjxLj > div > div.ShopNavigation-styles__ProfileActions-sc-b599f1d4-2.iGCycd > div.ShopNavigation-styles__ProfileActionsLeft-sc-b599f1d4-4.iAyRuq > div:nth-child(2) > button').click()
    time.sleep(3)
    global completed
    completed = 1
    while completed < listingCount:
        while True:
            try:
                driver.find_element(By.CSS_SELECTOR, f'#products-tab > div > ul > li:nth-child({completed}) > div > div.styles__ProductImageContainer-sc-9691b5f-3.TlTNt > a > div > div > div > div > img.sc-htehQK.fmdgqI').click()
                time.sleep(3)
                imgCount = 1
                for i in range(10):
                    try:
                        with open(f'{imgCount}.png', 'wb') as file:
                            img = driver.find_element(By.CSS_SELECTOR, f'#main > div.styles__Layout-sc-76cbd7e-2.fxYZcS > div.styles__Desktop-sc-93cf0ef1-1.gDHfTG > div:nth-child({imgCount}) > img')
                            url = img.get_attribute('src')
                            response = requests.get(url, stream=True)
                            shutil.copyfileobj(response.raw, file)
                            print(f'Saved {url} successfuly.')
                        del response
                        imgCount +=1
                        time.sleep(0.5)
                    except:
                        break   
            except:
                break
            print(f'Saved {imgCount-1} images successfuly, continuing to listing.')
            driver.find_element(By.CSS_SELECTOR, '#main > div.styles__Layout-sc-76cbd7e-2.fxYZcS > div.styles__ContentWrapper-sc-76cbd7e-3.esxDgq > div.ProductOwner-styles__Wrapper-sc-436f5c15-0.dJzVRH.styles__StyledProductOwner-sc-76cbd7e-16.kSSqjS > a.sc-jrkPvW.btSkUl.ProductOwner-styles__ButtonCopy-sc-436f5c15-4.PZjrL').click()
            time.sleep(5)
            uploadCount = 1
            for i in range(imgCount-1):
                driver.find_element(By.CSS_SELECTOR, '#imageInput').send_keys(os.getcwd()+f"/{uploadCount}.png")
                print(f'Uploaded {uploadCount}/{imgCount-1} files.')
                os.remove(f'{uploadCount}.png')
                uploadCount +=1
                time.sleep(4)
            print(f'{uploadCount-1} images successfuly uploaded.')
            os.remove(f'{imgCount}.png') #photos fully uploaded
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR, '#selectLocation__countries__select').send_keys('United States')
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR, '#selectLocation__countries__select').send_keys(Keys.ENTER)
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR, '#selectLocation__cities__select').send_keys('San Jose')
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR, '#selectLocation__cities__select').send_keys(Keys.ENTER)
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR, '#main > form > div.styles__SubmitButtonsContainer-sc-2b412d69-0.hMVIOz > button').click()
            print(f'Succesfuly saved, {completed}/{listingCount} to drafts.')
            completed+=1
            time.sleep(0.2)
            driver.get(f'https://depop.com/{username}')
    print(f'Complete! Successfuly saved {completed}/{listingCount} to drafts.')

    




def deleteActive(driver):
    time.sleep(3)
    deletedCount = 1
    for i in range(listingCount):
        driver.find_element(By.CSS_SELECTOR, f'#products-tab > div > ul > li:nth-child(1) > div > div.styles__ProductImageContainer-sc-9691b5f-3.TlTNt > a > div > div > div > div > img.sc-htehQK.fmdgqI').click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, '#main > div.styles__Layout-sc-76cbd7e-2.fxYZcS > div.styles__ContentWrapper-sc-76cbd7e-3.esxDgq > div.ProductOwner-styles__Wrapper-sc-436f5c15-0.dJzVRH.styles__StyledProductOwner-sc-76cbd7e-16.kSSqjS > button.sc-jrkPvW.btSkUl.ProductOwner-styles__ButtonDelete-sc-436f5c15-1.bFfdoP').click()
        time.sleep(0.2)
        driver.find_element(By.CSS_SELECTOR, 'body > div.sc-WSdTW.hIlmbX > div > aside > div.styles__ModalInner-sc-4153936c-1.cbNqtb > footer > button.sc-jrkPvW.gpscWh.styles__ConfirmButton-sc-4153936c-3.jyHMEV').click()
        print(f'Deleted {deletedCount/listingCount}')
        deletedCount +=1
        driver.get(f'https://depop.com/{username}')
        time.sleep(3)
    print(f'Deleted all {deletedCount}/{listingCount} items, posting drafts now.')


def postDrafts(driver):
    posted = 0
    driver.get('https://www.depop.com/sellinghub/drafts/readyToPost/')
    time.sleep(3)
    for i in range(listingCount):
        driver.find_element(By.CSS_SELECTOR, '#undefined-tab > div > div > div:nth-child(1) > section > div > div.styles__TextContainer-sc-38fd6c77-2.jsAznx > div > div.styles__ActionWrapper-sc-38fd6c77-7.fNiDrh > button.sc-jrkPvW.eiIIwx.styles__PostButton-sc-38fd6c77-8.fBWSth').click()
        posted +=1
        print(f'{posted}/{listingCount} drafts posted.')
        time.sleep(10)
    print(f'Done! All current listings successfuly relisted! ({posted}/{listingCount})')


def clearAccount(driver):
    print('Error, clearing account and restarting.')
    time.sleep(3)
    c = 1
    for i in range(10):
        try:
            os.remove(f'{c}.png')
            c+=1
        except:
            continue
    driver.get('https://www.depop.com/sellinghub/drafts/readyToPost/')
    time.sleep(5)
    c=1
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, '#undefined-tab > div > div > div:nth-child(1) > section > div > div.styles__TextContainer-sc-38fd6c77-2.jsAznx > div > div.styles__ActionWrapper-sc-38fd6c77-7.fNiDrh > button.styles__StyledDeleteButton-sc-38fd6c77-11.eLUOmm').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'body > div.sc-WSdTW.hIlmbX > div > aside > div.styles__ModalInner-sc-4153936c-1.cbNqtb > footer > button.sc-jrkPvW.gpscWh.styles__ConfirmButton-sc-4153936c-3.jyHMEV').click()
            print(f'Deleted {c} draft.')
            time.sleep(3)
            c+=1
        except:
            print('All drafts successfuly deleted, re-trying relistings.')
            break
    

def initialize():
    global driver
    service = webdriver.ChromeService(executable_path = '/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service)



username = os.environ['username']
email = os.environ['email']
password = os.environ['password']

initialize()
login(email, password, driver)

while True:
    try:
        relist(driver)
        deleteActive(driver)
        postDrafts(driver)
        print(f"Successfuly relisted {username}'s entire account")
        break
    except:
        clearAccount(driver)



