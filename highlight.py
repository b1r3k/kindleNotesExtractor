from datetime import datetime
import re

HIGHLIGHT_SEP = '=========='

def joinlines(lines):
	'''
	Joins lines contained in interable. Adds line seperator!
	'''
	seperated_lines = [ line + '\n' for line in lines ]

	return ''.join(seperated_lines)

def get_highlight(highlights_input):

	highlight_str = ""

	for line in highlights_input:
		if line.strip() == HIGHLIGHT_SEP:
			yield highlight_str
			highlight_str = ""

		else:
			highlight_str += line

def extract_highlights(highlights_input):
	"""
	Extract all highlights in a given file
	highlights_input - input descriptor

	returns dict where key is book title and value is dict of highlights (key = page no., value = Highlight)

	dict[book_title] = { page_no: Highlight }
	
	"""

	all_highlights = {}

	for highlight in get_highlight(highlights_input):
		highlight_obj = Highlight()
		highlight_obj.parse_highlight(highlight)
		
		try:
			all_highlights[highlight_obj.book_title][highlight_obj.page_no] = highlight_obj

		except KeyError:
			all_highlights[highlight_obj.book_title] = {}
			
			all_highlights[highlight_obj.book_title][highlight_obj.page_no] = highlight_obj

	return all_highlights


class Highlight(object):
	book_title = None
	page_no = None
	location = None
	date_added = None
	quote = None
	author = None

	def __init__(self):
		self.book_title = None
		self.page_no = None
		self.location = None
		self.date_added = None
		self.quote = None

	def __str__(self):
		str = "Book title: %s\n"
		str += "Added on: %s\n"
		str += "Page no. %d & location: %s\n"
		str += "\nQuote: %s\n"

		return str % (self.book_title, self.date_added)

	def parse_highlight(self, highlight_string):
		"""
		"""
		highlight_lines = highlight_string.splitlines()

		# remove empty lines
		stripped_highlight_lines = [ line.strip() for line in highlight_lines ]

		highlight_lines = []
		for line in stripped_highlight_lines:
			if len(line) > 0:
				highlight_lines.append(line)  

		# extract author name contained in the same line as book title but in parentheses
		author_match = re.search('[(](.*?)[)]', highlight_lines[0])
		self.author = author_match.group(1)

		# extract book title but get rid of author name
		self.book_title = highlight_lines[0][:author_match.start()].strip()

		page_str, location_str, date_str = highlight_lines[1].split('|')

		# remove 'Added on' from date string
		date_str = date_str.strip()[9:]

		# extract pg. no from '- Highlight on Page X '
		page_str = re.search('\d+', page_str).group(0)

		self.page_no = int(page_str)
		
		# extract Loc no.
		loc_no = re.findall('\d+', location_str)

		self.location = (int(loc_no[0]), int(loc_no[1]))

		# extract date
		self.date_added = datetime.strptime(date_str, "%A, %B %d, %Y, %I:%M %p")

		quote_str = highlight_lines[2:]

		self.quote = joinlines( quote_str )

		return
