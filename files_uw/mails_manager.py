from people import *

def mails_finder(list_people, dict_company):
	ptr_cell = list_people.head
	dict_unknown = {}
	for cellule_cpt in range(list_people.len):
		ptr_people = ptr_cell.people
		ablaye = True
		if ptr_people.email != 'x3':
			ablaye = False
		company_get = ptr_people.company
		company_transcript = company_get.lower().replace(" ", "")
		if company_transcript in dict_company.keys():
			if "xfname" in dict_company[company_transcript]: #Adresse mail du type john.smith@company.net
				ptr_people.email = dict_company[company_transcript].replace("xfname", ptr_people.firstname).replace("xlname", ptr_people.lastname)
			elif "yfname" in dict_company[company_transcript]: #Adresse mail du type j.smith@company.net
				ptr_people.email = dict_company[company_transcript].replace("yfname", ptr_people.firstname[0]).replace("xlname", ptr_people.lastname)
			else: #Adresse mail unique
				ptr_people.email = dict_company[company_transcript]
			ablaye = False
		if company_transcript in dict_unknown.keys():
			ablaye = False
		if ablaye:
			dict_unknown[company_transcript] = company_get
		if ptr_cell.next != None:
			ptr_cell = ptr_cell.next
	if len(dict_unknown) > 0 :
		mail_finder(dict_unknown)
		dict_company.update(dict_unknown)
		mails_finder(list_people, dict_company)


def mail_finder(dictionnaire):
	for company in dictionnaire.keys():
		print("Company : ", dictionnaire[company])
		mail_struct = input("Mail :") #format John.Smith@company.net
		if "John" in mail_struct:
			dictionnaire[company] = mail_struct.replace("John", "xfname").replace("Smith", 'xlname')
		elif "F1N1L" in mail_struct:
			dictionnaire[company] = mail_struct.replace("F1N1L", "yfname").replace("Smith", 'xlname')
		else:
			dictionnaire[company] = mail_struct