from people import *
from scraper_neverbounce_v2 import *

def mails_finder(list_people, dict_company):
	ptr_cell = list_people.head
	dict_unknown = {}
	for cellule_cpt in range(list_people.len):
		ptr_people = ptr_cell.people
		if ptr_people.email != 'x3':
			continue
		company_get = ptr_people.company
		company_transcript = company_get.lower().replace(" ", "")
		if company_transcript in dict_company.keys():
			ptr_people.email = dict_company[company_transcript].replace("123", ptr_people.firstname).replace("456", ptr_people.lastname)
			continue
		if company_transcript in dict_unknown.keys():
			continue
		dict_unknown[company_transcript] = company_get
		if ptr_cell.next != None:
			ptr_cell = ptr_cell.next
	if len(dict_unknown) > 0 :
		neverbounce_scraper_mail(dict_unknown)
		dict_company.update(dict_unknown)
		mails_finder(list_people, dict_company)




