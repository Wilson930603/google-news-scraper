from urllib.parse import urljoin
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By as by
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
import pandas as pd
from time import sleep
from datetime import datetime
import os

STARTDATE  = "24/06/2023"  #Enter Start Date of Date Range in dd/mm/yyyy
ENDDATE = "24/06/2023" #Enter End Date od Date Range in dd/mm/yyyy
filename = "GoogleNews.csv" #Enter Output File Path

from webdriver_manager.chrome import ChromeDriverManager
PATH = ChromeDriverManager().install()

def getdriver():
    '''
    A Function For Chrome Driver Settings
    '''
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('useAutomationExtension', False)

    executable_path=(PATH)
    driver = Chrome(
        executable_path=executable_path,
        options=chrome_options)
    return driver

def dateInRange(date,startdate,enddate,format="%d/%m/%Y",isScrapAll = False):
    '''
    A Utility Function To Check If the Article Date is in Required Date Range
    Send isScrapAll True if You want to scrap all articles without date filter
    '''
    if not isScrapAll:
        datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        try:
            startdate_obj = datetime.strptime(startdate,format)
            enddate_obj = datetime.strptime(enddate,format)
        except:
            print(f"The Start Date {startdate} or End Date {enddate} Format Doesnt Match With dd/mm/yyyy")
        if startdate_obj.date() <= datetime_obj.date() <= enddate_obj.date():
            return True
        else:
            return False
    else:
        return True
    




'''
Main Parse Page Function 
'''

driver = getdriver()
driver.get("https://news.google.com/home?hl=en-CA&gl=CA&ceid=CA:en")
response = Selector(driver.page_source)
newstypes = [urljoin("https://news.google.com/",u) for u in response.xpath("//div[contains(@class,'EctEBd')]/a[contains(@href,'topic')]/@href").extract()]

for news in newstypes:
    driver.get(news)
    sleep(.5)
    newssubtypes = driver.find_elements(by.XPATH,"//div[@class = 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb']/button[@role = 'tab']")
    if newssubtypes != []:
        for i in  range(0,len(newssubtypes)):
            newssubtypes = driver.find_elements(by.XPATH,"//div[@class = 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb']/button[@role = 'tab']")
            newssubtypes[i].click()
            sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            response = Selector(driver.page_source)
            for article in response.xpath("//c-wiz[@jsrenderer = 'ARwRbe']/c-wiz/div/article | //div[@class = 'f9uzM']/article | //c-wiz[@jsrenderer = 'ARwRbe']/c-wiz/article"):
                title = article.xpath(".//h4/text()").get().strip()
                source = article.xpath(".//div/div/div/div[@class = 'vr1PYe']/text()").get()
                date = article.xpath(".//div/time/@datetime").get()
                link = urljoin("https://news.google.com/",article.xpath(".//div/a/@href").get())
                frame = {"Headline":[],
                        "NewsSource":[],
                        "Link":[],
                        "DatePosted":[],}
                if dateInRange(date,STARTDATE,ENDDATE):
                    frame['Headline'].append(title)
                    frame['NewsSource'].append(source)
                    frame['Link'].append(link)
                    frame['DatePosted'].append(date)
                    if not os.path.exists(filename):
                        pd.DataFrame(frame).to_csv(filename,index = False)
                    else:
                        pd.DataFrame(frame).to_csv(filename,index = False,mode = 'a',header = False) 
                    print(frame) 
            driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);") 
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        response = Selector(driver.page_source)
        for article in response.xpath("//c-wiz[@jsrenderer = 'ARwRbe']/c-wiz/div/article | //div[@class = 'f9uzM']/article | //c-wiz[@jsrenderer = 'ARwRbe']/c-wiz/article"):
            title = article.xpath(".//h4/text()").get().strip()
            source = article.xpath(".//div/div/div/div[@class = 'vr1PYe']/text()").get()
            date = article.xpath(".//div/time/@datetime").get()
            link = urljoin("https://news.google.com/",article.xpath(".//div/a/@href").get())
            frame = {"Headline":[],
                    "NewsSource":[],
                    "Link":[],
                    "DatePosted":[],}
            
            if dateInRange(date,STARTDATE,ENDDATE):
                frame['Headline'].append(title)
                frame['NewsSource'].append(source)
                frame['Link'].append(link)
                frame['DatePosted'].append(date)
                if not os.path.exists(filename):
                    pd.DataFrame(frame).to_csv(filename,index = False)
                else:
                    pd.DataFrame(frame).to_csv(filename,index = False,mode = 'a',header = False)
                print(frame)
pd.read_csv(filename).drop_duplicates().to_csv(filename,index=False)
driver.close()