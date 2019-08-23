import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import random
import json
import codecs

def get_company_name(driver, company_list):
    def getInfoFromHTML(html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('tbody')

        for tr in table.children:

            td_name = list(tr.children)[2]
            name_tag = td_name.find('a')
            name = name_tag.text
            company_list.append(name)


    flag = True
    while flag:
        time.sleep(random.randint(1, 5))
        company_table = driver.find_element_by_xpath('//*[@id="table_wrapper-table"]')
        table_html = company_table.get_attribute('innerHTML')
        getInfoFromHTML(table_html)

        # page = driver.find_element_by_xpath('//*[@id="main-table_paginate"]')
        # next_button = page.find_element_by_class_name('next paginate_button')
        try:
            next_button = driver.find_element_by_xpath('//*[@id="main-table_paginate"]/a[2]')
            ActionChains(driver).move_to_element(next_button).perform()
            next_button.click()
        except:
            flag = False

def gethref(driver):
    href_tag = driver.find_element_by_xpath('//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div[1]/div/div[3]/div[1]/a')
    href = href_tag.get_attribute('href')

    return href
def main():
    chromedriver_path = '/Users/mxb/Desktop/chromedriver'
    driver = webdriver.Chrome(chromedriver_path)
    driver.get('https://www.tianyancha.com/search?key=科陆电子')
    gethref(driver)
    driver.get('http://quote.eastmoney.com/center/gridlist.html#hs_a_board')
    company_list = []
    get_company_name(driver, company_list)
    #
    company_dict = {}
    for name in company_list:
        url = 'https://www.tianyancha.com/search?key=' + name
        driver.get(url)
        href = gethref(driver)
        company_dict[name] = href

    json_file = codecs.open('company.json', 'w', 'utf-8')
    json.dump(company_dict, json_file, indent=2)




if __name__ == '__main__':
    main()
