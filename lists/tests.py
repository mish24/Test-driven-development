from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_returns_correct_html(self):
		request = HttpResponse()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content) #you made an error by writing contents. check and improve. it would then give an assertionerror and not an attribute error
		#self.assertTrue(response.content.endswith(b'</html>'))
		#we did this because sometimes there's a problem with the text editor
		self.assertTrue(response.content.strip().endswith(b'</html>'))
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		#decode converts response.content into the unicode string, which allows us to compare string with strings. 

#now that one class test works, lets create one more test to see whether the right template is rendered or not

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		#this actually calls the function under test
		#to pass this test, we just need to add a request.post thing in the view. nothing else
		response = home_page(request)
		
		self.assertIn('A new list item', response.content.decode())
		#we are giving the variable new_item_list whose value is expected to ne the text, the first parameter is the html which is to be manually rendered and compared to the html the view returns
		expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
		self.assertEqual(response.content.decode(), expected_html)
