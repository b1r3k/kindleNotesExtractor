import unittest
from datetime import datetime

import highlight

class TestHighlightHelpers(unittest.TestCase):

	def setUp(self):
		self.basic_file_input = open("tests/inputs/basic_clippings.txt", "r")

	def test_highlight_yielding(self):
		expected_highlight_first_line = (	"THIS IS TITLE AAAA (Author Name)",
											"THIS IS TITLE BBBB (Author Name)",
											"THIS IS TITLE CCCC (Author Name)",
										)
		line_no = 0

		for highlight_str in highlight.get_highlight(self.basic_file_input):
			highlight_lines = highlight_str.splitlines()

			self.assertEqual(highlight_lines[0], expected_highlight_first_line[line_no])

			line_no += 1
		
	def test_extraction_len(self):
		
		extracted_highlights = highlight.extract_highlights( self.basic_file_input )

		self.assertEqual(len(extracted_highlights.keys()), 3)

	# def test_extraction_

class TestHighlightCorrect(unittest.TestCase):
	correct_input = """THIS IS TITLE (Author Name)
					- Highlight on Page 97 | Loc. 1478-79  | Added on Monday, October 29, 2012, 11:59 PM

					This is highlight for book: THIS IS TITLE at page 97
					This is second line
					... and third one
					"""

	def setUp(self):
		self.highlighter = highlight.Highlight()
		self.highlighter.parse_highlight(self.correct_input)

	def test_highlight_title_extraction(self):
		
		self.assertEqual(self.highlighter.book_title, "THIS IS TITLE")

	def test_highlight_author(self):
		self.assertEqual(self.highlighter.author, 'Author Name')

	def test_highlight_page_no(self):

		self.assertEqual(self.highlighter.page_no, 97 )

	def test_highlight_location(self):

		self.assertEqual(self.highlighter.location, (1478, 79) )

	def test_highlight_date(self):
		ref_dt = datetime.strptime('Monday, October 29, 2012, 11:59 PM', "%A, %B %d, %Y, %I:%M %p")

		self.assertEqual(self.highlighter.date_added, ref_dt)

	def test_highlight_quote(self):
		expected_quote = 'This is highlight for book: THIS IS TITLE at page 97\nThis is second line\n... and third one\n'
		
		self.assertEqual(expected_quote, self.highlighter.quote)
