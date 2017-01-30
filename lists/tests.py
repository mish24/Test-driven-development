from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string


from lists.models import Item

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
	def test_home_page_can_save_a_post_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		# objects.first() is the same as objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_home_page_redirects_after_post(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'] , '/lists/the-only-list-in-the-world/')
		
	def test_home_page_only_saves_non_empty(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)

#next we test hte models
class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		#we create an object of the item
		first_item.text = 'The first (ever) list item'
		first_item.save()
		#we save the object
	
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 1)
	
		first_saved_item = saved_items[0]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')

class ListViewTest(TestCase):
	
	def test_displays_all_items(self):
		Item.objects.create(text = 'itemey 1')
		Item.objects.create(text = 'itemey 2')
		
		response = self.client.get('/lists/the-only-list-in-the-world/')
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')
		
#for the new list item entry, we would like to use the django test client
class NewListIten(TestCase):
	
	def test_saving_a_post_request(self):
		data = {'item_text': 'A new list item',}
		self.client.post('/lists/new', data)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_to_the_correct_url_after_post(self):
		data = {'item_text': 'A new list item',}
		response = self.client.post('/lists/new', data)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
