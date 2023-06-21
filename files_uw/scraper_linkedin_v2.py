from people import *
from private_credits import Myemail, Linkedin_password
from langdetect import detect

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from linkedin_scraper import actions

def getting_infos_list(list_people, list_url):
	driver = webdriver.Chrome()
	try:
		actions.login(driver, Myemail, Linkedin_password)
	except:
		print('Remplir le captcha Linkedin')

	for link in list_url:
		current_people = getting_infos(link, driver)
		cell_current = People_cell(current_people)
		list_people.append(cell_current)

	driver.quit()


def getting_infos(url_people, driver):
	driver.get(url_people)
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "pvs-list")))
	people2send = People()

	try:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	except:
		print("Impossible d'effectuer des actions sur la page chargée")

	main = driver.find_element(By.TAG_NAME, 'main')
	sections = main.find_elements(By.TAG_NAME, 'section')

	#Recuperation post et names
	section = sections[0]
	text = section.text
	list_text = text.split('\n')
	
	people2send.lastname = ''.join(list_text[0].split(' ')[1:])
	people2send.firstname = list_text[0].split(' ')[0]

	people2send.post = list_text[3]

	#Recuperation about
	about_exist = False

	for section in sections[1:]:
		fr_about = 'Infos' in section.text
		en_about = 'About' in section.text
		if fr_about or en_about:
			about_exist = True
			break

	if about_exist:
		people2send.about = ' '.join(section.text.split('\n')[2:-1])
	
	#Recuperation experience

	#url_experience = url_people + '/details/experience'
	#driver.get(url_experience)
	#time.sleep(5)

	#main = driver.find_element(By.TAG_NAME, 'main')
	last_exp = main.find_element(By.CLASS_NAME, 'pvs-list')

	fr_current = "aujour" in last_exp.text
	en_current = "present" in last_exp.text

	if fr_current or en_current:
		people2send.company = last_exp.find_element(By.TAG_NAME, 'img').get_attribute('alt')[8:]

	#Predire la langue
	if about_exist:
		language = detect(people2send.about)
		if (language == 'en') or (language == 'fr'):
			people2send.language = language
		else:
			people2send.language = 'en'
	else:
		people2send.language = 'en'

	return people2send










