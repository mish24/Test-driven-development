#to check from the point of view of a user
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_new_list_and_retrieve_it_later(self):
		#let's check out the homepage
		self.browser.get('http://localhost:8000')
		
	#you notice that the title and header are mentioned
		self.assertIn('To-Do', self.browser.title)
		
		#next, we check whether the header we talked about is pro=esent or not. ALso, doe it have right info
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		#you are really invited to enter a new item to the list
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
		#you type get gsoc into the textbox
		inputbox.send_keys('Get GSoC')
		#when you hit tinter, only then the page updates
		inputbox.send_keys(Keys.ENTER)
		
		
		#next we move to the next element, which tells us about the table
		#remember, sometimes we need to just find the element, other times we need to access whats inside that specific id
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		#we add the second argument as the error message
		self.assertIn('8 : Get GSoC', [row.text for row in rows])
		#there is still a text box inviting you to add another item. 
		#for later
		

		
		
		
if __name__ == '__main__':
	unittest.main()
