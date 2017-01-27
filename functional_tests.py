from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest (unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		#you learnt about a new cool website and you went online to check it out
		self.browser.get('http://localhost:8000')
		
		#you should notice the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		#you are invited to enter a to-do item straightaway
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
		
		#she types "Buy peacock feathers" into the text box
		inputbox.send_keys('Buy peacock feathers')
		
		#when she hits enter, the page updates and now the page lists 1: Buy peacock feathers
		inputbox.send_keys(Keys.ENTER)
		
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.asserttrue(any(row.text == '1: Buy peacock feathers' for row in rows)
		
		#there still is a box to invite her to enter another item, she enters "Use peacock feathers to make a fly"

		
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')
	#for the reminder, the name and main thing ensures that the program is run from the command line and not from any other script
