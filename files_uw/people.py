import base64
from neverbounce_scraper import mail_getter

class People:
	def __init__(self):
		self.lastname = 'x1'
		self.firstname = 'x2'
		self.email = 'x3'
		self.company = 'x4'
		self.post = 'x5'
		self.language = 'x6'
		self.about = 'x7'
		self.sent = False
		self.__id = [0,b'0']
	
	def setter(self, lastname, firstname, email, company, post, lang):
		self.lastname = lastname
		self.firstname = firstname
		self.email = email
		self.company = company
		self.post = post
		self.language = lang

	def email_setter(self, email=None):
		if email:
			self.email = email
		else:
			self.email_setter(email=mail_getter(self.lastname, self.firstname, self.company))

	def id_setter(self):
		if(self.lastname == 'x1'):
			return self.__id
		else:
			source = self.lastname + self.firstname + self.company
			hashed = base64.b64encode(source.encode())
			if(len(hashed.decode())>8):
				shorted_hashed = hashed.decode()[:7]
				digit = sum(hashed)
			self.__id = [digit, shorted_hashed]
		return [digit, shorted_hashed]

	def id_getter(self):
		return self.__id

class People_cell :
	def __init__(self, people):
		self.people = people
		self.pred = None
		self.next = None

	def insert(self, pred_cell):
		self.pred = pred_cell
	
	def gluer(self, next_cell):
		self.next = next_cell

class People_list:
	def __init__(self):
		self.head = None
		self.tail = None
		self.len = 0
		self.list_id = []

	def append(self, people_cell):
		id_people = people_cell.people.id_setter()

		if id_people in self.list_id:
			print('Deja existant ID : ', id_people)
			return

		self.list_id.append(id_people)

		if self.len == 0:
			self.head = people_cell
			self.tail = people_cell
			self.len = 1
		else:
			self.len += 1
			people_cell.insert(self.tail)
			self.tail.gluer(people_cell)
			self.tail = people_cell



