from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

def google_url_generator(query_str):
    query_list = query_str.split(" ")
    return 'https://www.google.com/search?q=' + '+'.join(query_list)

def link_scraper(links_list, driver):
    links = driver.find_elements(By.XPATH, value='//a[@href]')
    for link in links:
        ref_link = link.get_attribute("href")
        if('linkedin.com/in' in ref_link):
            links_list.append(link.get_attribute("href"))

def linkedin_link_scraper(links_list, URL):
	#Ouverture du driver chrome
	driver = webdriver.Chrome()
	driver.get(URL)
	time.sleep(0.2)

	#Passer les cookies
	try:
		driver.find_element(By.ID, 'L2AGLb').click()
	except:
		print('No cookies pass needed')
	time.sleep(0.2)

	#Scraping SERP google result sur toutes les pages accessibles
	max_page = 10
	cpt_page = 0

	while cpt_page < max_page:
		cpt_page += 1
		link_scraper(links_list, driver)

		#Tente de passer a la page suivante
		try:
			driver.find_element(By.ID, value='pnnext').click()
    	except:
        	break
        time.sleep(0.2)
	
	driver.quit()